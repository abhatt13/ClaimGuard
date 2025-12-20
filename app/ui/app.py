"""
ClaimGuard Gradio Dashboard
Interactive UI for insurance claims processing and fraud detection
"""

import gradio as gr
import pandas as pd
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.core.config import settings
from app.models.claim import Claim
from app.models.fraud_score import FraudScore
from app.models.policy import Policy
from app.services.ai.vision_analyzer import get_vision_analyzer


# Database connection
engine = create_engine(settings.DATABASE_URL)


def get_claims_overview():
    """Get overview statistics"""
    session = Session(engine)

    total_claims = session.query(Claim).count()
    high_risk = session.query(FraudScore).filter(FraudScore.fraud_score >= 0.5).count()
    pending_review = session.query(Claim).filter(Claim.status == 'PROCESSING').count()

    total_value = session.query(Claim.estimated_damage).count()

    session.close()

    return f"""
    ### 📊 ClaimGuard Dashboard

    **Total Claims:** {total_claims:,}

    **High-Risk Claims:** {high_risk:,} ({high_risk/total_claims*100:.1f}%)

    **Pending Review:** {pending_review:,}

    **Total Estimated Damages:** ${total_value:,.2f}
    """


def load_claims_data(risk_filter="all", limit=100):
    """Load claims data with filters"""

    session = Session(engine)

    query = session.query(
        Claim.claim_number,
        Claim.claim_type,
        Claim.status,
        Claim.estimated_damage,
        FraudScore.fraud_score,
        FraudScore.risk_level,
        Policy.policy_number
    ).join(FraudScore).join(Policy)

    if risk_filter == "high_risk":
        query = query.filter(FraudScore.fraud_score >= 0.5)
    elif risk_filter == "medium_risk":
        query = query.filter(FraudScore.fraud_score >= 0.3, FraudScore.fraud_score < 0.5)
    elif risk_filter == "low_risk":
        query = query.filter(FraudScore.fraud_score < 0.3)

    query = query.order_by(desc(FraudScore.fraud_score)).limit(limit)

    df = pd.read_sql(query.statement, session.bind)

    session.close()

    # Format columns
    if len(df) > 0:
        df['fraud_score'] = df['fraud_score'].apply(lambda x: f"{x:.3f}")
        df['estimated_damage'] = df['estimated_damage'].apply(lambda x: f"${x:,.2f}")
        df.columns = ['Claim #', 'Type', 'Status', 'Estimated Damage', 'Fraud Score', 'Risk Level', 'Policy #']

    return df


def get_claim_details(claim_number):
    """Get detailed information about a claim"""

    if not claim_number:
        return "Enter a claim number to view details"

    session = Session(engine)

    claim = session.query(Claim).filter(Claim.claim_number == claim_number).first()

    if not claim:
        session.close()
        return f"❌ Claim {claim_number} not found"

    fraud_score = session.query(FraudScore).filter(FraudScore.claim_id == claim.id).first()

    details = f"""
    ## Claim Details: {claim.claim_number}

    **Status:** {claim.status.value}
    **Priority:** {claim.priority.value}
    **Type:** {claim.claim_type.value}

    ### Incident Information
    **Date:** {claim.incident_date}
    **Location:** {claim.incident_location}
    **Description:** {claim.description}

    ### Financial
    **Estimated Damage:** ${claim.estimated_damage:,.2f}
    **Deductible:** ${claim.deductible:,.2f}

    ### Fraud Assessment
    **Fraud Score:** {fraud_score.fraud_score:.3f}
    **Risk Level:** {fraud_score.risk_level}
    **Requires Investigation:** {"Yes" if fraud_score.requires_investigation else "No"}

    **Fraud Flags:** {', '.join(fraud_score.fraud_flags) if fraud_score.fraud_flags else 'None'}

    ### Model Information
    **ML Score:** {fraud_score.ml_model_score:.3f}
    **Graph Score:** {fraud_score.graph_network_score:.3f}
    **Pattern Score:** {fraud_score.pattern_matching_score:.3f}
    """

    session.close()

    return details


def analyze_damage_image(image):
    """Analyze uploaded damage image"""

    if image is None:
        return "Please upload an image to analyze"

    try:
        analyzer = get_vision_analyzer()

        # Convert gradio image to bytes
        from PIL import Image
        import io

        if isinstance(image, str):
            # File path
            result = analyzer.analyze_damage(image)
        else:
            # numpy array from gradio
            pil_image = Image.fromarray(image)
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()

            result = analyzer.analyze_damage(img_bytes)

        if result.get('success'):
            output = f"""
            ### ✅ Damage Assessment Complete

            **Damage Types:** {', '.join(result.get('damage_types', []))}

            **Severity:** {result.get('severity')}

            **Severity Score:** {result.get('severity_score')}/100

            **Affected Areas:** {', '.join(result.get('affected_areas', []))}

            **Estimated Cost:** ${result.get('cost_estimate', {}).get('min', 0):,.2f} - ${result.get('cost_estimate', {}).get('max', 0):,.2f}

            **Notes:** {result.get('notes', 'N/A')}

            ---
            *Model: {result.get('model')}*

            *Tokens Used: {result.get('usage', {}).get('total_tokens', 0)}*
            """
            return output
        else:
            return f"❌ Analysis failed: {result.get('error')}"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="ClaimGuard - AI Insurance Claims Processing", theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🛡️ ClaimGuard
    ## AI-Powered Insurance Claims Processing & Fraud Detection
    """)

    with gr.Tab("📊 Dashboard"):
        overview = gr.Markdown(get_claims_overview())
        gr.Button("🔄 Refresh").click(get_claims_overview, outputs=overview)

        gr.Markdown("### Recent Claims")

        risk_filter = gr.Radio(
            choices=["all", "high_risk", "medium_risk", "low_risk"],
            value="all",
            label="Filter by Risk Level"
        )

        claims_table = gr.Dataframe(
            value=load_claims_data(),
            label="Claims",
            interactive=False
        )

        risk_filter.change(load_claims_data, inputs=risk_filter, outputs=claims_table)

    with gr.Tab("🔍 Claim Details"):
        gr.Markdown("### Search Claim")

        claim_input = gr.Textbox(
            label="Enter Claim Number",
            placeholder="e.g., CLM-1994-000001"
        )

        claim_details_output = gr.Markdown()

        gr.Button("🔍 Search").click(
            get_claim_details,
            inputs=claim_input,
            outputs=claim_details_output
        )

    with gr.Tab("📸 Damage Assessment"):
        gr.Markdown("""
        ### Vehicle Damage Assessment
        Upload an image of vehicle damage for AI analysis
        """)

        with gr.Row():
            with gr.Column():
                damage_image = gr.Image(
                    label="Upload Damage Photo",
                    type="numpy"
                )

                analyze_btn = gr.Button("🔍 Analyze Damage", variant="primary")

            with gr.Column():
                damage_results = gr.Markdown(label="Assessment Results")

        analyze_btn.click(
            analyze_damage_image,
            inputs=damage_image,
            outputs=damage_results
        )

        gr.Markdown("""
        **Note:** This uses OpenAI Vision API (gpt-4o-mini)

        **Cost:** ~$0.0006 per image
        """)

    with gr.Tab("📈 Analytics"):
        gr.Markdown("### Fraud Detection Analytics")

        session = Session(engine)

        # Risk distribution
        risk_dist = pd.read_sql("""
            SELECT
                risk_level,
                COUNT(*) as count,
                AVG(fraud_score) as avg_score
            FROM fraud_scores
            GROUP BY risk_level
            ORDER BY
                CASE risk_level
                    WHEN 'low' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'high' THEN 3
                    WHEN 'critical' THEN 4
                END
        """, session.bind)

        session.close()

        gr.Dataframe(
            value=risk_dist,
            label="Risk Level Distribution"
        )

    gr.Markdown("""
    ---
    **ClaimGuard v1.0** | Powered by OpenAI Vision & XGBoost
    """)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🛡️  Starting ClaimGuard Dashboard")
    print("="*60)
    print(f"\n📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")
    print(f"🤖 AI Model: {settings.OPENAI_VISION_MODEL}")
    print("\n" + "="*60 + "\n")

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
