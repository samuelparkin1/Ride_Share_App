from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.riders import Rider
import boto3
from flask_login import login_required, current_user

rider_images = Blueprint('rider_images', __name__)

@rider_images.route("/riders/<int:id>/image/", methods=["POST"])
@login_required
def update_image(id):

    rider = Rider.query.get_or_404(id)
    
    # if "image" in request.files:
        
    #     image = request.files["image"]
        
    #     if Path(image.filename).suffix != ".png":
    #         return abort(400, description="Invalid file type")
        
    #     bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    #     bucket.upload_fileobj(image, rider.image_filename)


    #     return redirect(url_for("riders.get_rider", id=id))

    return abort(400, description="No image")
