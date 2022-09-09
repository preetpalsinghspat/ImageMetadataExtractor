from flask import Flask, request, redirect, url_for, render_template
from PIL import Image, IptcImagePlugin
from PIL.ExifTags import TAGS
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        image = request.files['image']
        extension = image.filename.split('.')[-1]
        image.filename = f'image.{extension}'
        img_path = f'uploaded_files/{image.filename}'
        image.save(img_path)
        img = Image.open(img_path)

        img_data = dict()
        iptc_data = []
        exif_data = []

        img_data['image_info'] = [
            f"Filename : {img.filename}",
            f"Image Size : {img.size}",
            f"Image Height : {img.height}",
            f"Image Width : {img.width}",
            f"Image Format : {img.format}",
            f"Image Mode : {img.mode}",
            f"Image is Animated : {getattr(img, 'is_animated', False)}",
            f"Frames in Image : {getattr(img, 'n_frames', 1)}"
        ]

        iptc = IptcImagePlugin.getiptcinfo(img)
        exifdata = img.getexif()

        # adding iptc data to list
        if iptc:
            for k, v in iptc.items():
                if isinstance(v, bytes):
                    try:
                        iptc_data.append(f"{k} :  {v.decode()}")
                    except UnicodeDecodeError as e:
                        iptc_data.append(f"{k} :  {v}")
                else:
                    iptc_data.append(f"{k} :  {v}")
        else:
            iptc_data.append('No iptc data present')

        # adding exif data to list
        if exifdata:
            for tag_id, data in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                if isinstance(data, bytes):
                    data = data.decode()
                exif_data.append(f"{tag} :  {data}")
        img_data['iptc'] = iptc_data
        img_data['exif'] = exif_data
        return render_template('final.html', img_info=img_data)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
