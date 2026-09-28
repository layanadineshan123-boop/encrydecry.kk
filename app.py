
import streamlit as st
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Secure File Vault",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #172033;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #667085;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.success-box {
    background: #ecfdf3;
    padding: 15px;
    border-radius: 10px;
    color: #067647;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: #667085;
    margin-top: 40px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">🔐 Secure File Vault</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Securely encrypt and decrypt your files using password-based encryption</div>',
    unsafe_allow_html=True
)

# ---------------- KEY FUNCTION ----------------
def generate_key(password):
    password_hash = hashlib.sha256(
        password.encode()
    ).digest()

    return base64.urlsafe_b64encode(password_hash)


# ---------------- TABS ----------------
encrypt_tab, decrypt_tab = st.tabs(
    ["🔒 Encrypt File", "🔓 Decrypt File"]
)

# ==================================================
# ENCRYPTION
# ==================================================

with encrypt_tab:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔒 Encrypt Your File")

    uploaded_file = st.file_uploader(
        "Choose a file to encrypt",
        key="encrypt_file"
    )

    password = st.text_input(
        "Create Encryption Password",
        type="password",
        key="encrypt_password"
    )

    if st.button(
        "🔐 Encrypt File",
        use_container_width=True
    ):

        if uploaded_file is None:
            st.error("⚠️ Please select a file.")

        elif not password:
            st.error("⚠️ Please enter a password.")

        else:

            try:
                file_data = uploaded_file.read()

                key = generate_key(password)
                cipher = Fernet(key)

                encrypted_data = cipher.encrypt(file_data)

                original_name = uploaded_file.name
                encrypted_name = original_name + ".encrypted"

                st.success("✅ File encrypted successfully!")

                st.download_button(
                    label="⬇️ Download Encrypted File",
                    data=encrypted_data,
                    file_name=encrypted_name,
                    mime="application/octet-stream",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Encryption error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# DECRYPTION
# ==================================================

with decrypt_tab:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔓 Decrypt Your File")

    encrypted_file = st.file_uploader(
        "Choose an encrypted file",
        key="decrypt_file"
    )

    decrypt_password = st.text_input(
        "Enter Encryption Password",
        type="password",
        key="decrypt_password"
    )

    if st.button(
        "🔓 Decrypt File",
        use_container_width=True
    ):

        if encrypted_file is None:
            st.error("⚠️ Please select an encrypted file.")

        elif not decrypt_password:
            st.error("⚠️ Please enter the password.")

        else:

            try:
                encrypted_data = encrypted_file.read()

                key = generate_key(decrypt_password)
                cipher = Fernet(key)

                decrypted_data = cipher.decrypt(
                    encrypted_data
                )

                original_name = encrypted_file.name

                if original_name.endswith(".encrypted"):
                    original_name = original_name[:-10]
                else:
                    original_name = "decrypted_" + original_name

                st.success("✅ File decrypted successfully!")

                st.download_button(
                    label="⬇️ Download Decrypted File",
                    data=decrypted_data,
                    file_name=original_name,
                    mime="application/octet-stream",
                    use_container_width=True
                )

            except InvalidToken:
                st.error(
                    "❌ Incorrect password or corrupted encrypted file."
                )

            except Exception as e:
                st.error(f"Decryption error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class="footer">
        Secure File Vault • Python + Streamlit + Fernet Encryption<br>
        Your password is not stored by this application.
    </div>
    """,
    unsafe_allow_html=True
)