import base64
import os
from playwright.sync_api import sync_playwright

def render_pdf_to_images(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(pdf_path, "rb") as f:
        pdf_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
        <style>
            body {{ margin: 0; background: white; }}
            canvas {{ display: block; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            const pdfData = atob("{pdf_b64}");
            const loadingTask = pdfjsLib.getDocument({{ data: pdfData }});
            
            async function renderAll() {{
                const pdf = await loadingTask.promise;
                window.totalPages = pdf.numPages;
                const container = document.getElementById('container');
                
                for (let i = 1; i <= pdf.numPages; i++) {{
                    const page = await pdf.getPage(i);
                    const viewport = page.getViewport({{ scale: 2.0 }});
                    const canvas = document.createElement('canvas');
                    canvas.id = 'page-' + i;
                    canvas.width = viewport.width;
                    canvas.height = viewport.height;
                    container.appendChild(canvas);
                    
                    const context = canvas.getContext('2d');
                    await page.render({{
                        canvasContext: context,
                        viewport: viewport
                    }}).promise;
                }}
                window.renderingDone = true;
            }}
            renderAll();
        </script>
    </body>
    </html>
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        page.wait_for_function("window.renderingDone === true", timeout=30000)
        
        num_pages = page.evaluate("window.totalPages")
        image_paths = []
        for i in range(1, num_pages + 1):
            canvas_el = page.query_selector(f"#page-{i}")
            img_path = os.path.join(output_dir, f"halaman-{i}.png")
            canvas_el.screenshot(path=img_path)
            image_paths.append(img_path)
            print(f"Rendered Page {i} -> {img_path}")
        browser.close()
    return image_paths

if __name__ == "__main__":
    images = render_pdf_to_images("lomba/essay-civil-comp/draf/draf-v5.pdf", "lomba/essay-civil-comp/draf/halaman_preview")
    print(f"Total rendered: {len(images)} pages")
