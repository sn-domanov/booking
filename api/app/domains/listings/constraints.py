from app.db.exceptions import ConstraintConflict

CONSTRAINT_MAP = {
    "uq_listing_image_position": ConstraintConflict(
        conflict="listing_image_position",
        detail="A listing image already exists at this position.",
    ),
}
