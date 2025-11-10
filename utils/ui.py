
import streamlit as st

def load_css():
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def header(title: str, subtitle: str = ""):
    html = f"""
    <div class='card' style="padding:18px 16px;">
      <h2 style="margin:0 0 4px 0;">🍽️ {title}</h2>
      <p class='small-muted' style="margin:0;">{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
def footer_nav():
    st.markdown(
        '''
        <div class="footer-nav">
            <div class="wrap">
                <a href="/">🏠 Home</a>
                <a href="/Test_Library">🔎 Tests</a>
                <a href="/Quiz">🧪 Quiz</a>
                <a href="/My_Results">📒 Results</a>
                <a href="/Admin_Panel">⚙️ Admin</a>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

def load_css():
    # your existing code...


def header():
    # your existing code...


def footer_nav():
    # your existing code...


# 👉 PASTE THE NEW FUNCTION HERE
def top_nav(go):
    """Apple-like top nav that calls the router 'go' with page keys."""
    st.markdown(
        """
        <div class="apple-nav apple-font">
          <div class="wrap">
            <div class="brand">DART</div>
            <div class="links">
              <a class="link" href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;">Tests</a>
              <a class="link" href="#" onclick="window.parent.postMessage({type:'route',page:'quiz'}, '*'); return false;">Quiz</a>
              <a class="link" href="#" onclick="window.parent.postMessage({type:'route',page:'results'}, '*'); return false;">Results</a>
              <a class="link" href="#" onclick="window.parent.postMessage({type:'route',page:'admin'}, '*'); return false;">Admin</a>
            </div>
          </div>
        </div>
        <script>
        window.addEventListener('message', (e)=>{
          const d = e.data||{};
          if(d.type==='route' && d.page){
            const qs = new URLSearchParams(window.location.search);
            qs.set('goto', d.page);
            window.location.search = qs.toString();
          }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )
    goto = st.query_params.get("goto")
    if goto:
        st.query_params.clear()
        go(goto)
