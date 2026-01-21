from flask import Blueprint, jsonify
from models.model_category import ModelCategory

model_categories_bp = Blueprint('model_categories', __name__)

@model_categories_bp.route('/model_categories', methods=['GET'])
def get_model_categories():
    categories = ModelCategory.query.all()
    return jsonify([category.to_dict() for category in categories])
