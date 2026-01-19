import gradio as gr
from app.brochure_generator import generate_brochure_stream

with gr.Blocks(title="AI Website Brochure Generator") as demo:
    gr.Markdown("## 🧠 AI Website Brochure Generator")

    url = gr.Textbox(label="Website URL")
    category = gr.Dropdown(
        choices=["Professional", "Sarcastic"],
        value="Professional"
    )

    max_links = gr.Slider(0, 50, value=20)
    max_chars = gr.Slider(1000, 15000, value=6000)

    btn = gr.Button("Generate")
    output = gr.Markdown()

    btn.click(
        generate_brochure_stream,
        inputs=[url, max_links, max_chars, category],
        outputs=output,
    )
