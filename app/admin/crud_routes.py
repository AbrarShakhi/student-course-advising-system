from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.core.db import db
from sqlalchemy.inspection import inspect


def generate_crud_routes(model, blueprint_name):
    bp = Blueprint(blueprint_name, __name__)

    pk_keys = [key.name for key in inspect(model).primary_key]

    @bp.route("/", methods=["POST"])
    @jwt_required()
    def create_item():
        try:
            data = request.get_json()
            item = model(**data)
            db.session.add(item)
            db.session.commit()
            return (
                jsonify(
                    {"message": f"{model.__name__} created", "data": serialize(item)}
                ),
                201,
            )
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Create {model.__name__} failed: {e}")
            return jsonify({"error": str(e)}), 400

    @bp.route("/", methods=["GET"])
    @jwt_required()
    def get_all():
        items = model.query.all()
        return jsonify([serialize(i) for i in items])

    @bp.route("/<path:pk>", methods=["GET"])
    @jwt_required()
    def get_one(pk):
        filters = parse_pk(pk, pk_keys)
        item = model.query.filter_by(**filters).first_or_404()
        return jsonify(serialize(item))

    @bp.route("/<path:pk>", methods=["PUT", "PATCH"])
    @jwt_required()
    def update_item(pk):
        try:
            filters = parse_pk(pk, pk_keys)
            item = model.query.filter_by(**filters).first_or_404()
            data = request.get_json()
            for key, value in data.items():
                setattr(item, key, value)
            db.session.commit()
            return jsonify({"message": f"{model.__name__} updated"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @bp.route("/<path:pk>", methods=["DELETE"])
    @jwt_required()
    def delete_item(pk):
        try:
            filters = parse_pk(pk, pk_keys)
            item = model.query.filter_by(**filters).first_or_404()
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"{model.__name__} deleted"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    return bp


def serialize(obj):
    """Convert SQLAlchemy object to dict"""
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def parse_pk(pk, pk_keys):
    """Parse single or composite PK"""
    pk_parts = pk.split(",")
    if len(pk_parts) != len(pk_keys):
        raise ValueError("Primary key parts mismatch")
    return dict(zip(pk_keys, pk_parts))
