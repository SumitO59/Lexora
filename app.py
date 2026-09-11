import os
import tempfile
import streamlit as st
from pathlib import Path

from src import RAGEngine, OLLAMA_MODEL

st.set_page_config(
    page_title="Lexora · Local RAG",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #0f1117; }
  .badge        { display:inline-block; padding:2px 8px; border-radius:4px;
                  font-size:11px; font-weight:600; letter-spacing:.4px; }
  .badge-green  { background:#1a3a2a; color:#4ade80; border:1px solid #22c55e33; }
  .badge-blue   { background:#1a2a3a; color:#60a5fa; border:1px solid #3b82f633; }
  .answer-box   { background:#161b22; border:1px solid #30363d;
                  border-radius:8px; padding:16px 20px; margin-top:8px; }
  .source-tag   { background:#1e2d3d; color:#7dd3fc; border-radius:4px;
                  padding:2px 7px; font-size:12px; margin-right:4px; }
  .entity-pill  { display:inline-block; background:#1a2a1a; color:#86efac;
                  border:1px solid #22c55e44; border-radius:12px;
                  padding:1px 9px; font-size:12px; margin:2px; }
  .num-pill     { display:inline-block; background:#2a1a2a; color:#d8b4fe;
                  border:1px solid #a855f744; border-radius:12px;
                  padding:1px 9px; font-size:12px; margin:2px; }
  .summary-box  { background:#0d1117; border-left:3px solid #3b82f6;
                  padding:10px 14px; border-radius:4px; font-size:14px;
                  color:#cbd5e1; margin-bottom:8px; }
  .citation {
    background:#111827;
    border:1px solid #374151;
    border-radius:10px;
    padding:12px;
    margin-top:8px;
    margin-bottom:8px;
  }
  .passage {
    color:#cbd5e1;
    margin-top:8px;
    font-size:13px;
    line-height:1.5;
  }
  .score-bar-bg { background:#21262d; border-radius:4px; height:6px; margin-top:4px; }
  .score-bar    { background:#3b82f6; border-radius:4px; height:6px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading models…")
def get_engine():
    return RAGEngine()


engine = get_engine()

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("Lexora")
    st.markdown(
        '<span class="badge badge-green">● 100% Local</span> '
        '<span class="badge badge-blue">No API calls</span>',
        unsafe_allow_html=True,
    )
    st.divider()

    model = st.selectbox(
        "Ollama model",
        ["llama3", "mistral", "phi3", "gemma2"],
    )
    k = st.slider("Chunks to retrieve (k)", 2, 8, 4)
    st.divider()

    st.markdown("### Upload Documents")
    uploads = st.file_uploader(
        "PDF, DOCX, TXT, MD, XLSX",
        type=["pdf", "docx", "txt", "md", "xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploads:
        for f in uploads:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=Path(f.name).suffix,
            ) as tmp:
                tmp.write(f.read())
                tmp_path = tmp.name

            with st.spinner(f"Indexing + analysing {f.name}…"):
                res = engine.index_file(
                    tmp_path,
                    original_name=f.name,
                    model=model,
                )
                os.unlink(tmp_path)

            if res["ok"]:
                st.success(res["msg"])
                a = res["analysis"]
                st.markdown(
                    f'<div class="summary-box">{a["summary"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.error(res["msg"])

    st.divider()
    stats = engine.stats()
    st.markdown(
        f"**Indexed files** ({stats['total_chunks']} chunks)"
    )

    if stats["files"]:
        for fname in sorted(stats["files"]):
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"`{fname}`")

            if col2.button("✕", key=f"del_{fname}"):
                engine.delete_file(fname)
                st.rerun()
    else:
        st.caption("No documents indexed yet.")

    st.divider()

    if st.button("🗑 Clear chat history"):
        st.session_state.history = []
        st.rerun()


tab_chat, tab_docs = st.tabs(["Chat", "Document Insights"])

with tab_chat:
    st.markdown("## Ask your documents")
    st.caption(
        "All processing happens locally. Zero data leaves your machine."
    )

    if st.session_state.history:
        for item in reversed(st.session_state.history):
            q, a, srcs, citations = item

            with st.chat_message("user"):
                st.write(q)

            with st.chat_message("assistant"):
                st.markdown(
                    f'<div class="answer-box">{a}</div>',
                    unsafe_allow_html=True,
                )

                if srcs:
                    src_html = " ".join(
                        f'<span class="source-tag">{s}</span>'
                        for s in srcs
                    )
                    st.markdown(
                        f"**Sources:** {src_html}",
                        unsafe_allow_html=True,
                    )

                if citations:
                    with st.expander(
                        f"Sources ({len(citations)})",
                        expanded=False,
                    ):
                        for i, c in enumerate(citations, 1):
                            pct = max(
                                0,
                                min(
                                    100,
                                    int(c["score"] * 100),
                                ),
                            )

                            page = c.get("page")

                            if page is not None:
                                page_text = f"Page {page + 1}"
                            else:
                                page_text = ""

                            passage = " ".join(
                                c["passage"].split()
                            )

                            st.markdown(
                                f"""
**[{i}] {c['source']}**

{page_text} | Confidence {pct}%
"""
                            )

                            st.caption(passage[:250])
                            st.divider()

    question = st.chat_input(
        "Ask something about your documents…"
    )

    if question:
        if stats["total_chunks"] == 0:
            st.warning("Upload at least one document first.")
        else:
            with st.spinner("Thinking…"):
                result = engine.query(
                    question,
                    model=model,
                    k=k,
                )

            st.session_state.history.append(
                (
                    question,
                    result["answer"],
                    result["sources"],
                    result["citations"],
                )
            )

            st.rerun()


with tab_docs:
    st.markdown("## Document Insights")
    all_meta = engine.all_meta()

    if not all_meta:
        st.info(
            "Upload documents to see auto-generated summaries, "
            "entities, and key numbers."
        )
    else:
        for fname, meta in all_meta.items():
            with st.expander(
                f"{fname}  —  {meta.get('chunks', '?')} chunks",
                expanded=True,
            ):
                st.markdown("**Summary**")
                st.markdown(
                    f'<div class="summary-box">'
                    f'{meta.get("summary", "—")}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                col_ent, col_num = st.columns(2)

                with col_ent:
                    st.markdown("**Key Entities**")
                    ents = meta.get("entities", {})

                    for category, items in ents.items():
                        if items:
                            st.markdown(
                                f"*{category.capitalize()}*"
                            )

                            pills = " ".join(
                                f'<span class="entity-pill">{e}</span>'
                                for e in items
                            )

                            st.markdown(
                                pills,
                                unsafe_allow_html=True,
                            )

                with col_num:
                    st.markdown("**Key Numbers**")
                    nums = meta.get("key_numbers", [])

                    if nums:
                        for n in nums:
                            val = n.get("value", "")
                            ctx = n.get("context", "")

                            st.markdown(
                                f'<span class="num-pill">{val}</span> '
                                f'<span style="color:#94a3b8;'
                                f'font-size:13px">{ctx}</span>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.caption("No key numbers found.")
