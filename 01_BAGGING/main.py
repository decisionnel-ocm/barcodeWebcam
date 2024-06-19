import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")
        return self.frame


def read_barcode(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Decode the barcodes in the image
    barcodes = decode(image)

    # Iterate over all detected barcodes
    for barcode in barcodes:
        # Extract the bounding box coordinates
        (x, y, w, h) = barcode.rect
        # Draw a rectangle around the barcode
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # The barcode data is a bytes object, so we convert it to a string
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        return barcode_data, barcode_type

def main():
    st.title("Webcam Snapshot with Streamlit")
    
    webrtc_ctx = webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        media_stream_constraints={"video": True, "audio": False},
    )

    if webrtc_ctx.video_transformer:
        if st.button("Take a snapshot"):
            frame = webrtc_ctx.video_transformer.frame
            if frame is not None:
                st.image(frame, channels="BGR")
                # Save the image if needed
                cv2.imwrite("snapshot.png", frame)
                st.success("Snapshot saved!")
    
    if st.button("Print Barcode"):
        barcode_data, barcode_type = read_barcode("snapshot.png")
        st.write(barcode_data)

if __name__ == "__main__":
    main()
