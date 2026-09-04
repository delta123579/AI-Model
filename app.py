import os
import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored posts with captions and hashtags powered by Groq.")

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.info("💡 Please enter your Groq API Key to proceed.")
    api_key = st.text_input("Groq API Key:", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # Input form
    with st.form("content_form"):
        col1, col2 = st.columns(2)

        with col1:
            content_type = st.selectbox(
                "Content Type",
                ["Social Media Post", "Blog Post Intro", "Email Newsletter", "Ad Copy"]
            )
            platform = st.selectbox(
                "Platform",
                ["LinkedIn", "Twitter/X", "Instagram", "Facebook", "Medium"]
            )
            tone = st.selectbox(
                "Tone",
                ["Professional", "Casual & Friendly", "Persuasive", "Informative", "Witty"]
            )

        with col2:
            topic = st.text_input("Topic", placeholder="e.g. Benefits of Remote Work")
            target_audience = st.text_input("Target Audience", placeholder="e.g. Software Engineers, Small Business Owners")

        submit = st.form_submit_button("Generate Post", use_container_width=True)

    # Output generation logic
    if submit:
        if not topic or not target_audience:
            st.warning("Please fill out both the Topic and Target Audience fields.")
        else:
            with st.spinner("Generating your post..."):
                prompt = f"""
                You are a professional social media and content specialist.
                Create a complete post using these specifications:

                - Content Type: {content_type}
                - Target Platform: {platform}
                - Topic: {topic}
                - Target Audience: {target_audience}
                - Tone: {tone}

                Your output MUST strictly follow this structure:
                1. **Post Title / Headline**
                2. **Main Post Content** (Formatted properly with emojis if appropriate for the platform)
                3. **Caption** (Short, engaging 1-2 sentence caption or call-to-action)
                4. **Hashtags** (5-10 relevant, high-performing hashtags)
                """

                try:
                    # Using Groq's fast Llama model
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )

                    generated_content = response.choices[0].message.content

                    st.markdown("---")
                    st.subheader("🚀 Generated Content")
                    st.markdown(generated_content)

                except Exception as e:
                    st.error(f"Error generating content: {e}")
else:
    st.warning("Add your `GROQ_API_KEY` to continue.")
