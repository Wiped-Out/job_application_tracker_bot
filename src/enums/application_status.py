from enum import Enum


class ApplicationStatus(Enum):
    """Possible application status."""

    applied = 'applied'
    interviewing = 'interviewing'
    negotiating = 'negotiating'
    accepted = 'accepted'
    declined = 'declined'
    rejected = 'rejected'
    archived = 'archived'
