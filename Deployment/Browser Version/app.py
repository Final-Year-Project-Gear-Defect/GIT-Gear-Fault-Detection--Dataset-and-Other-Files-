import streamlit as st
import cv2
import numpy as np
import time
from ultralytics import YOLO

# Load YOLO model
@st.cache_resource
def load_model():
    return YOLO("best.pt")  # make sure best.pt is in same folder

model = load_model()

# Class colors
class_colors = {"kp": (0, 255, 255), "hp_cm": (255, 0, 255), "hp_cd": (128, 0, 255)}

def predict_and_overlay(img):
    result = model.predict(source=img, imgsz=640, conf=0.25, save=False)[0]
    image = result.orig_img.copy()

    for box in result.obb:
        cls_id = int(box.cls[0])
        label = result.names[cls_id]
        pts = box.xyxyxyxy[0].cpu().numpy().astype(int).reshape(-1, 2)

        overlay = image.copy()
        cv2.fillPoly(overlay, [pts], class_colors[label])
        image = cv2.addWeighted(overlay, 0.4, image, 0.6, 0)
        cv2.polylines(image, [pts], isClosed=True, color=class_colors[label], thickness=2)
        x, y = pts[0]
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, class_colors[label], 2)

    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="⚙️ Gear Fault Detection", page_icon="🛠", layout="centered")
st.title("⚙️ Gear Fault Detection Software")

uploaded_file = st.file_uploader("📂 Upload Gear Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Convert uploaded file to image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Show uploaded image
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="📸 Uploaded Image", use_column_width=True)

    if st.button("🔍 Run Detection"):
        with st.spinner("🔄 Detecting faults... Please wait"):
            time.sleep(1)
            result_img = predict_and_overlay(img)

        st.success("✅ Detection Completed!")
        st.image(result_img, caption="🛠 Detection Result", use_column_width=True)

        # Save + Download button
        save_path = "detection_result.jpg"
        cv2.imwrite(save_path, cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))
        with open(save_path, "rb") as f:
            st.download_button("⬇️ Download Result", f, file_name="gear_fault_result.jpg", mime="image/jpeg")
