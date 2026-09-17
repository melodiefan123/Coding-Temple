# app-frontend/components/card_dialog.py
import json
import os
import requests
import streamlit as st


@st.dialog("➕ Add New Credit Card")
def add_card_dialog(api_url: str, headers: dict):
    with st.form("add_card_form", clear_on_submit=True):
        card_name = st.text_input("Card Name / Label", placeholder="e.g. Chase Sapphire Preferred")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            full_card_num = st.text_input("Card Number", max_chars=19, placeholder="1234 5678 9012 3456")
        with col2:
            exp_date = st.text_input("Expiration (MM/YY)", max_chars=5, placeholder="08/28")

        col3, col4, col5 = st.columns([1.5, 1.5, 1.5])
        with col3:
            card_type = st.selectbox("Card Type", ["Visa", "Mastercard", "American Express", "Discover", "Other"])
        with col4:
            credit_limit = st.number_input("Credit Limit ($)", min_value=0.0, step=100.0)
        with col5:
            current_balance = st.number_input("Current Balance ($)", min_value=0.0, step=50.0)

        submitted = st.form_submit_button("Save Card", use_container_width=True)

        if submitted:
            clean_card_num = "".join(filter(str.isdigit, full_card_num))
            
            if not card_name:
                st.error("Please provide a card name/label.")
            elif len(clean_card_num) < 13 or len(clean_card_num) > 19:
                st.error("Please enter a valid card number (13-19 digits).")
            elif not exp_date or "/" not in exp_date or len(exp_date.strip()) != 5:
                st.error("Please enter expiration date in MM/YY format (e.g. 08/28).")
            else:
                last_four = clean_card_num[-4:]
                
                payload = {
                    "card_name": card_name,
                    "card_type": card_type,
                    "last_four": last_four,
                    "expiration_date": exp_date.strip(),
                    "credit_limit": credit_limit,
                }
                
                try:
                    response = requests.post(f"{api_url}/cards/", json=payload, headers=headers)
                    if response.status_code in [200, 201]:
                        st.toast(f"Successfully added {card_name} (•••• {last_four})!", icon="💳")
                        st.rerun()
                    else:
                        st.error(f"Failed to save card: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")


def get_card_theme(card_type: str) -> tuple[str, str, str]:
    c_type = (card_type or "").lower()
    if "visa" in c_type:
        return "linear-gradient(135deg, #1A1F71 0%, #2A38A8 100%)", "VISA", "#0e131f"
    elif "mastercard" in c_type:
        return "linear-gradient(135deg, #1E1E1E 0%, #3A3A3A 100%)", "MC", "#121212"
    elif "american" in c_type or "amex" in c_type:
        return "linear-gradient(135deg, #8A7322 0%, #C5A028 100%)", "AMEX", "#1c180a"
    elif "discover" in c_type:
        return "linear-gradient(135deg, #944400 0%, #E65C00 100%)", "DISCOVER", "#211003"
    else:
        return "linear-gradient(135deg, #2B3A42 0%, #3F5159 100%)", "CARD", "#111618"


def load_local_gsap() -> str:
    possible_paths = [
        os.path.join("static", "gsap.min.js"),
        os.path.join(os.path.dirname(__file__), "..", "static", "gsap.min.js"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return ""


def render_interactive_cards(cards: list, api_url: str, headers: dict):
    if not cards:
        st.info("No credit cards added yet. Click 'Add Card' to link your first card!")
        return None

    

    local_gsap_code = load_local_gsap()
    if local_gsap_code:
        gsap_script_tag = f"<script>{local_gsap_code}</script>"
    else:
        gsap_script_tag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>'

    formatted_cards = []
    for card in cards:
        bg, badge, ambient_bg = get_card_theme(card.get("card_type", ""))
        bal_val = float(card.get("current_balance", 0.0))
        formatted_cards.append({
            "id": card.get("id"),
            "name": (card.get("card_name") or "Card").upper(),
            "badge": badge,
            "last_four": card.get("last_four", "••••"),
            "exp_date": card.get("expiration_date") or "N/A",
            "balance": f"{bal_val:,.2f}",
            "background": bg,
            "ambient_bg": ambient_bg
        })

    cards_json = json.dumps(formatted_cards)
    headers_json = json.dumps(headers)

    gsap_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        {gsap_script_tag}
        <script>
            // Streamlit Component API helper
            function sendToStreamlit(value) {{
                if (window.Streamlit) {{
                    window.Streamlit.setComponentValue(value);
                }}
            }}
        </script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                padding: 12px 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #605D5C !important;
                border-radius: 24px; 
                border: 1px solid rgba(255, 255, 255, 0.12);
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow: hidden; 
            }}

            .controls {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 24px;
                z-index: 1000;
            }}

            .btn {{
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(8px);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 8px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                transition: all 0.2s ease;
            }}
            .btn:hover {{ background: rgba(255, 255, 255, 0.25); }}

            .stack-wrapper {{
                position: relative;
                width: 340px;
                height: 320px;
                perspective: 1000px;
            }}

            .card-face {{
                position: absolute;
                bottom: 44px;
                left: 0;
                width: 340px;
                height: 190px;
                border-radius: 16px;
                padding: 22px;
                color: white;
                box-shadow: 0 14px 35px rgba(0, 0, 0, 0.45);
                transform-origin: center bottom;
                user-select: none;
                transition: filter 0.4s ease;
                will-change: transform, opacity, filter;
            }}

            .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px; }}
            .card-title {{ font-size: 14px; font-weight: 700; letter-spacing: 1px; }}

            .delete-btn {{
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                cursor: pointer;
                font-size: 13px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.2s;
            }}
            .delete-btn:hover {{ background: rgba(239, 68, 68, 0.9); }}

            .card-number {{ font-size: 18px; letter-spacing: 3px; font-weight: 600; margin-bottom: 20px; font-family: monospace; }}
            .card-footer {{ display: flex; justify-content: space-between; align-items: flex-end; }}
            .label {{ font-size: 9px; opacity: 0.75; text-transform: uppercase; letter-spacing: 0.5px; }}
            .val {{ font-size: 19px; font-weight: 700; }}
            .exp {{ font-size: 12px; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="controls">
            <button class="btn" onclick="rotateStack(-1)">🔼 Prev</button>
            <span id="cardCounter" style="color: rgba(255, 255, 255, 0.8); font-size: 12px; font-weight: 600;"></span>
            <button class="btn" onclick="rotateStack(1)">🔽 Next</button>
        </div>

        <div class="stack-wrapper" id="cardContainer"></div>

        <script>
            const cardsData = {cards_json};
            const apiUrl = "{api_url}";
            const apiHeaders = {headers_json};
            
            let cardElements = [];
            let isAnimating = false;

            function notifyActiveCard() {{
                if (cardElements.length > 0) {{
                    const activeCardId = cardElements[0]._cardData.id;
                    sendToStreamlit(activeCardId);
                }}
            }}

            function initStack() {{
                const container = document.getElementById("cardContainer");
                container.innerHTML = "";
                cardElements = [];

                if (cardsData.length === 0) return;

                cardsData.forEach((card) => {{
                    const el = document.createElement("div");
                    el.className = "card-face";
                    el.style.background = card.background;
                    el._cardData = card;

                    el.innerHTML = `
                        <div class="card-header">
                            <span class="card-title">${{card.name}}</span>
                            <button class="delete-btn" onclick="deleteCard(event, ${{card.id}}, '${{card.name}}')">🗑️</button>
                        </div>
                        <div class="card-number">•••• •••• •••• ${{card.last_four}}</div>
                        <div class="card-footer">
                            <div>
                                <div class="label">Current Balance</div>
                                <div class="val">$${{card.balance}}</div>
                            </div>
                            <div style="text-align: right;">
                                <div class="label">EXPIRES</div>
                                <div class="exp">${{card.exp_date}}</div>
                            </div>
                        </div>
                    `;

                    container.appendChild(el);
                    cardElements.push(el);
                }});

                applyStackStyles(false);
                updateCounter();
                notifyActiveCard();
            }}

            function updateCounter() {{
                const counter = document.getElementById("cardCounter");
                if (counter && cardElements.length > 0) {{
                    counter.innerText = `1 of ${{cardElements.length}}`;
                }}
            }}

            function applyStackStyles(animate = true) {{
                const total = cardElements.length;

                cardElements.forEach((el, idx) => {{
                    const yOffset = -(idx * 48); 
                    const scale = 1 - (idx * 0.035);
                    const blurValue = idx === 0 ? 0 : Math.min(idx * 2, 5);
                    const opacity = idx > 3 ? 0 : 1 - (idx * 0.15);
                    const zIndex = total - idx;

                    if (animate) {{
                        gsap.to(el, {{
                            duration: 0.46,
                            y: yOffset,
                            scale: scale,
                            opacity: opacity,
                            zIndex: zIndex,
                            filter: `blur(${{blurValue}}px)`,
                            ease: "power2.out"
                        }});
                    }} else {{
                        gsap.set(el, {{
                            y: yOffset,
                            scale: scale,
                            opacity: opacity,
                            zIndex: zIndex,
                            filter: `blur(${{blurValue}}px)`
                        }});
                    }}
                }});
            }}

            function rotateStack(direction) {{
                if (isAnimating || cardElements.length <= 1) return;
                isAnimating = true;

                if (direction === 1) {{
                    const topCard = cardElements.shift();

                    gsap.timeline({{
                        onComplete: () => {{
                            document.getElementById("cardContainer").appendChild(topCard);
                            cardElements.push(topCard);
                            applyStackStyles(true);
                            updateCounter();
                            notifyActiveCard();
                            isAnimating = false;
                        }}
                    }})
                    .to(topCard, {{
                        duration: 0.35,
                        y: 140,
                        scale: 0.85,
                        opacity: 0.2,
                        filter: "blur(6px)",
                        ease: "power2.in"
                    }});

                }} else {{
                    const bottomCard = cardElements.pop();
                    cardElements.unshift(bottomCard);

                    gsap.set(bottomCard, {{ zIndex: 999, filter: "blur(0px)" }});

                    gsap.fromTo(bottomCard, 
                        {{ y: 140, opacity: 0, scale: 0.85 }},
                        {{
                            duration: 0.4,
                            y: 0,
                            opacity: 1,
                            scale: 1,
                            ease: "power3.out",
                            onComplete: () => {{
                                applyStackStyles(true);
                                updateCounter();
                                notifyActiveCard();
                                isAnimating = false;
                            }}
                        }}
                    );
                }}
            }}

            async function deleteCard(event, cardId, cardName) {{
                event.stopPropagation();
                if (!confirm(`Delete ${{cardName}}?`)) return;

                try {{
                    const res = await fetch(`${{apiUrl}}/cards/${{cardId}}`, {{
                        method: 'DELETE',
                        headers: apiHeaders
                    }});

                    if (res.ok || res.status === 204) {{
                        window.parent.location.reload();
                    }}
                }} catch (e) {{
                    console.error("Delete failed", e);
                }}
            }}

            if (typeof gsap !== 'undefined') {{
                initStack();
            }} else {{
                window.addEventListener('load', initStack);
            }}
        </script>
    </body>
    </html>
    """

    st.markdown("""
    <style>
        div[data-testid="stIFrame"], 
        div[data-testid="stCustomComponentV1"],
        iframe[title="st.iframe"] {
            border-radius: 24px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4) !important;
            margin-top: -28px !important;
            margin-left: 10px !important;
            width: 130% !important; 
        }
    </style>
    """, unsafe_allow_html=True)

    # Use components.html with standard default fallback
    default_active_id = cards[0].get("id") if cards else None
    active_card_id = st.iframe(gsap_html, height=380)

    # Return active card ID (or fall back to first card)
    return active_card_id if active_card_id is not None else default_active_id