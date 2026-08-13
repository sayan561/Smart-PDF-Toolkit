
import streamlit as st
from pypdf import PdfWriter, PdfReader
from pdf2docx import Converter
from PIL import Image
import io
import tempfile
import os

# =========================
# PROFESSIONAL UI
# =========================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.tool-card {
    padding: 22px;
    border: 1px solid #dddddd;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="PDF Master Toolkit",
    page_icon="📄",
    layout="wide"
)


# =========================
# HEADER
# =========================
st.markdown(
    '<div class="main-title">📄 PDF Master Toolkit</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convert, compress and manage your PDF files easily'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================
# SIDEBAR
# =========================

st.sidebar.title("🛠️ PDF Tools")

tool = st.sidebar.radio(
    "Choose a Tool",
    [    
        "🏠 Home",
        "🔗 Merge PDF",
        "🗜️ Compress PDF",
        "📄 PDF → Word",
        "📝 PDF → Text",
        "🖼️ Images → PDF",
        "✂️ Split PDF",
        "🔄 Rotate PDF",
        "🗑️ Remove Pages",
        "🔀 Reorder PDF",
        "📝 Word → PDF"
    ]
)



# =========================
# HOME
# =========================

if tool == "🏠 Home":

    st.markdown(
        '<div class="main-title">📄 PDF Master Toolkit</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'All your PDF tools in one place'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🚀 What can you do?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="tool-card">'
            '<h3>🔗 Merge PDF</h3>'
            '<p>Combine multiple PDF files.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="tool-card">'
            '<h3>📄 PDF → Word</h3>'
            '<p>Convert PDF documents to Word.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="tool-card">'
            '<h3>🗜️ Compress PDF</h3>'
            '<p>Reduce PDF file size.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="tool-card">'
            '<h3>🖼️ Images → PDF</h3>'
            '<p>Convert images into PDF.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="tool-card">'
            '<h3>✂️ Split PDF</h3>'
            '<p>Extract selected pages.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="tool-card">'
            '<h3>🔄 Rotate PDF</h3>'
            '<p>Rotate PDF pages easily.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.success(
        "💡 Select any tool from the sidebar to get started."
    )






# =========================
# MERGE PDF
# =========================

elif tool == "🔗 Merge PDF":

    st.header("🔗 Merge PDF")

    files = st.file_uploader(
        "Upload multiple PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if files:

        st.success(f"✅ {len(files)} PDF files selected")

        if st.button("🔗 Merge PDFs", type="primary"):

            writer = PdfWriter()

            for file in files:
                writer.append(file)

            output = io.BytesIO()

            writer.write(output)
            writer.close()

            output.seek(0)

            st.success("✅ PDFs merged successfully!")

            st.download_button(
                "📥 Download Merged PDF",
                output.getvalue(),
                "merged.pdf",
                "application/pdf"
            )


# =========================
# COMPRESS PDF
# =========================

elif tool == "🗜️ Compress PDF":

    st.header("🗜️ Compress PDF")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        original_size = len(file.getvalue())

        st.info(
            f"📊 Original Size: "
            f"{original_size / 1024:.2f} KB"
        )

        if st.button("🗜️ Compress PDF", type="primary"):

            reader = PdfReader(file)
            writer = PdfWriter()

            for page in reader.pages:

                page.compress_content_streams()
                writer.add_page(page)

            output = io.BytesIO()

            writer.write(output)
            writer.close()

            compressed_data = output.getvalue()

            new_size = len(compressed_data)

            st.success("✅ Compression completed!")

            st.info(
                f"📦 New Size: "
                f"{new_size / 1024:.2f} KB"
            )

            if new_size < original_size:

                reduction = (
                    (original_size - new_size)
                    / original_size
                ) * 100

                st.success(
                    f"📉 Size reduced by "
                    f"{reduction:.1f}%"
                )

            else:

                st.warning(
                    "This PDF could not be reduced further."
                )

            st.download_button(
                "📥 Download Compressed PDF",
                compressed_data,
                "compressed.pdf",
                "application/pdf"
            )


# =========================
# PDF TO WORD
# =========================

elif tool == "📄 PDF → Word":

    st.header("📄 PDF → Word")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        st.success(f"📄 {file.name} selected")

        if st.button(
            "📄 Convert to Word",
            type="primary"
        ):

            pdf_path = None
            word_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_pdf:

                    temp_pdf.write(
                        file.getvalue()
                    )

                    pdf_path = temp_pdf.name

                temp_word = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".docx"
                )

                word_path = temp_word.name

                temp_word.close()

                converter = Converter(pdf_path)

                converter.convert(
                    word_path
                )

                converter.close()

                with open(
                    word_path,
                    "rb"
                ) as word_file:

                    word_data = word_file.read()

                st.success(
                    "✅ PDF converted to Word!"
                )

                st.download_button(
                    "📥 Download Word File",
                    word_data,
                    "converted.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            except Exception as e:

                st.error(
                    f"❌ Conversion failed: {e}"
                )

            finally:

                if pdf_path and os.path.exists(pdf_path):
                    os.remove(pdf_path)

                if word_path and os.path.exists(word_path):
                    os.remove(word_path)


# =========================
# PDF TO TEXT
# =========================

elif tool == "📝 PDF → Text":

    st.header("📝 PDF → Text")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        if st.button(
            "📝 Extract Text",
            type="primary"
        ):

            reader = PdfReader(file)

            all_text = []

            for number, page in enumerate(
                reader.pages,
                start=1
            ):

                text = page.extract_text()

                if text:

                    all_text.append(
                        f"--- Page {number} ---\n{text}"
                    )

            final_text = "\n\n".join(all_text)

            if final_text.strip():

                st.success(
                    "✅ Text extracted!"
                )

                st.text_area(
                    "📄 Extracted Text",
                    final_text,
                    height=400
                )

                st.download_button(
                    "📥 Download Text",
                    final_text,
                    "extracted_text.txt",
                    "text/plain"
                )

            else:

                st.warning(
                    "⚠️ No selectable text found."
                )


# =========================
# IMAGES TO PDF
# =========================

elif tool == "🖼️ Images → PDF":

    st.header("🖼️ Images → PDF")

    images = st.file_uploader(
        "Upload JPG or PNG images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images:

        st.success(
            f"🖼️ {len(images)} images selected"
        )

        if st.button(
            "🖼️ Convert to PDF",
            type="primary"
        ):

            image_list = []

            for uploaded_image in images:

                image = Image.open(
                    uploaded_image
                )

                if image.mode != "RGB":

                    image = image.convert(
                        "RGB"
                    )

                image_list.append(image)

            output = io.BytesIO()

            image_list[0].save(
                output,
                format="PDF",
                save_all=True,
                append_images=image_list[1:]
            )

            output.seek(0)

            st.success(
                "✅ Images converted to PDF!"
            )

            st.download_button(
                "📥 Download PDF",
                output.getvalue(),
                "images.pdf",
                "application/pdf"
            )


# =========================
# SPLIT PDF
# =========================

elif tool == "✂️ Split PDF":

    st.header("✂️ Split PDF")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        reader = PdfReader(file)

        total_pages = len(
            reader.pages
        )

        st.info(
            f"📄 Total Pages: {total_pages}"
        )

        page_range = st.text_input(
            "Enter page range",
            placeholder="Example: 1-3"
        )

        if st.button(
            "✂️ Split PDF",
            type="primary"
        ):

            try:

                start, end = page_range.split("-")

                start = int(start)
                end = int(end)

                if (
                    start < 1
                    or end > total_pages
                    or start > end
                ):

                    st.error(
                        "❌ Invalid page range."
                    )

                else:

                    writer = PdfWriter()

                    for page in range(
                        start - 1,
                        end
                    ):

                        writer.add_page(
                            reader.pages[page]
                        )

                    output = io.BytesIO()

                    writer.write(output)
                    writer.close()

                    output.seek(0)

                    st.success(
                        "✅ PDF split successfully!"
                    )

                    st.download_button(
                        "📥 Download Split PDF",
                        output.getvalue(),
                        "split.pdf",
                        "application/pdf"
                    )

            except:

                st.error(
                    "Enter range like 1-3"
                )


# =========================
# ROTATE PDF
# =========================

elif tool == "🔄 Rotate PDF":

    st.header("🔄 Rotate PDF")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        rotation = st.selectbox(
            "Choose Rotation",
            [
                90,
                180,
                270
            ]
        )

        if st.button(
            "🔄 Rotate PDF",
            type="primary"
        ):

            reader = PdfReader(file)

            writer = PdfWriter()

            for page in reader.pages:

                page.rotate(rotation)

                writer.add_page(page)

            output = io.BytesIO()

            writer.write(output)
            writer.close()

            output.seek(0)

            st.success(
                "✅ PDF rotated successfully!"
            )

            st.download_button(
                "📥 Download Rotated PDF",
                output.getvalue(),
                "rotated.pdf",
                "application/pdf"
            )


# =========================
# REMOVE PAGES
# =========================

elif tool == "🗑️ Remove Pages":

    st.header("🗑️ Remove PDF Pages")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        reader = PdfReader(file)

        total_pages = len(
            reader.pages
        )

        st.info(
            f"📄 Total Pages: {total_pages}"
        )

        pages = st.text_input(
            "Pages to remove",
            placeholder="Example: 2,4,6"
        )

        if st.button(
            "🗑️ Remove Pages",
            type="primary"
        ):

            try:

                remove_pages = {
                    int(x.strip())
                    for x in pages.split(",")
                }

                writer = PdfWriter()

                for number, page in enumerate(
                    reader.pages,
                    start=1
                ):

                    if number not in remove_pages:

                        writer.add_page(page)

                output = io.BytesIO()

                writer.write(output)
                writer.close()

                output.seek(0)

                st.success(
                    "✅ Pages removed successfully!"
                )

                st.download_button(
                    "📥 Download PDF",
                    output.getvalue(),
                    "pages_removed.pdf",
                    "application/pdf"
                )

            except:

                st.error(
                    "Enter page numbers like 2,4,6"
                )

# =========================
# REORDER PDF
# =========================

elif tool == "🔀 Reorder PDF":

    st.header("🔀 Reorder PDF Pages")

    file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if file:

        reader = PdfReader(file)
        total_pages = len(reader.pages)

        st.info(f"📄 Total Pages: {total_pages}")

        order = st.text_input(
            "Enter new page order",
            placeholder="Example: 3,1,2,4"
        )

        if st.button(
            "🔀 Reorder PDF",
            type="primary"
        ):

            try:

                page_order = [
                    int(x.strip())
                    for x in order.split(",")
                ]

                if len(page_order) != total_pages:

                    st.error(
                        f"Please enter exactly "
                        f"{total_pages} page numbers."
                    )

                elif sorted(page_order) != list(
                    range(1, total_pages + 1)
                ):

                    st.error(
                        "Use every page number exactly once."
                    )

                else:

                    writer = PdfWriter()

                    for page_number in page_order:

                        writer.add_page(
                            reader.pages[page_number - 1]
                        )

                    output = io.BytesIO()

                    writer.write(output)
                    writer.close()

                    output.seek(0)

                    st.success(
                        "✅ Pages reordered successfully!"
                    )

                    st.download_button(
                        "📥 Download Reordered PDF",
                        output.getvalue(),
                        "reordered.pdf",
                        "application/pdf"
                    )

            except ValueError:

                st.error(
                    "Enter page numbers like 3,1,2,4"
                )                

   # =========================
# WORD TO PDF
# =========================

elif tool == "📝 Word → PDF":

    st.header("📝 Word → PDF")

    file = st.file_uploader(
        "Upload a Word document",
        type=["docx"]
    )

    if file:

        st.success(f"📄 {file.name} selected")

        if st.button(
            "📝 Convert to PDF",
            type="primary"
        ):

            word_path = None
            pdf_path = None

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".docx"
                ) as temp_word:

                    temp_word.write(
                        file.getvalue()
                    )

                    word_path = temp_word.name

                pdf_path = word_path.replace(
                    ".docx",
                    ".pdf"
                )

                from docx2pdf import convert

                convert(
                    word_path,
                    pdf_path
                )

                with open(
                    pdf_path,
                    "rb"
                ) as pdf_file:

                    pdf_data = pdf_file.read()

                st.success(
                    "✅ Word converted to PDF!"
                )

                st.download_button(
                    "📥 Download PDF",
                    pdf_data,
                    "converted.pdf",
                    "application/pdf"
                )

            except Exception as e:

                st.error(
                    f"❌ Conversion failed: {e}"
                )

            finally:

                if word_path and os.path.exists(word_path):
                    os.remove(word_path)

                if pdf_path and os.path.exists(pdf_path):
                    os.remove(pdf_path)             


st.divider()

st.markdown("### ℹ️ About PDF Master Toolkit")

st.write(
    "PDF Master Toolkit is a simple all-in-one PDF utility "
    "app created for converting, merging, compressing and "
    "managing PDF documents."
)

st.info(
    "🔐 Your files are processed by the application and "
    "are not intended to be permanently stored."
)

st.divider()

st.markdown(
    '<div class="footer">'
    '📄 PDF Master Toolkit • Built with Python & Streamlit'
    '</div>',
    unsafe_allow_html=True
)                    