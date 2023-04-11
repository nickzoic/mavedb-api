# See https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
from __future__ import annotations
from datetime import date
from typing import Dict, Optional

from mavedb.view_models.base.base import BaseModel, validator
from mavedb.view_models.doi_identifier import DoiIdentifier, DoiIdentifierCreate, SavedDoiIdentifier
from mavedb.view_models.experiment import Experiment, SavedExperiment
from mavedb.view_models.license import License, SavedLicense, ShortLicense
from mavedb.view_models.pubmed_identifier import PubmedIdentifier, PubmedIdentifierCreate, SavedPubmedIdentifier
from mavedb.view_models.target_gene import SavedTargetGene, ShortTargetGene, TargetGene, TargetGeneCreate
from mavedb.view_models.user import SavedUser, User
from mavedb.view_models.variant import VariantInDbBase
from mavedb.lib.validation import keywords
from mavedb.lib.validation import urn


class ScoresetBase(BaseModel):
    """Base class for score set view models."""

    title: str
    method_text: str
    abstract_text: str
    short_description: str
    extra_metadata: Dict
    data_usage_policy: Optional[str]
    keywords: Optional[list[str]]


class ScoresetModify(ScoresetBase):
    @validator("keywords")
    def validate_keywords(cls, v):
        keywords.validate_keywords(v)
        return v


class ScoresetCreate(ScoresetModify):
    """View model for creating a new score set."""

    experiment_urn: str
    license_id: int
    superseded_scoreset_urn: Optional[str]
    meta_analysis_source_scoreset_urns: Optional[list[str]]
    target_gene: TargetGeneCreate
    doi_identifiers: Optional[list[DoiIdentifierCreate]]
    pubmed_identifiers: Optional[list[PubmedIdentifierCreate]]

    @validator("superseded_scoreset_urn", "meta_analysis_source_scoreset_urns")
    def validate_scoreset_urn(cls, v):
        if v is None:
            pass
        # For superseded_scoreset_urn
        elif type(v) == str:
            urn.validate_mavedb_urn_scoreset(v)
        # For meta_analysis_source_scoreset_urns
        else:
            [urn.validate_mavedb_urn_scoreset(s) for s in v]
        return v

    @validator("experiment_urn")
    def validate_experiment_urn(cls, v):
        urn.validate_mavedb_urn_experiment(v)
        return v


class ScoresetUpdate(ScoresetModify):
    """View model for updating a score set."""

    license_id: Optional[int]
    doi_identifiers: list[DoiIdentifierCreate]
    pubmed_identifiers: list[PubmedIdentifierCreate]
    target_gene: TargetGeneCreate


class ShortScoreset(BaseModel):
    """
    Score set view model containing a smaller set of properties to return in list contexts.

    Notice that this is not derived from ScoresetBase.
    """

    urn: str
    title: str
    short_description: str
    published_date: Optional[date]
    replaces_id: Optional[int]
    num_variants: int
    experiment: Experiment
    license: ShortLicense
    creation_date: date
    modification_date: date
    target_gene: ShortTargetGene
    private: bool

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SavedScoreset(ScoresetBase):
    """Base class for score set view models representing saved records."""

    urn: str
    num_variants: int
    experiment: SavedExperiment
    license: SavedLicense
    superseded_scoreset: Optional[ShortScoreset]
    superseding_scoreset: Optional[SavedScoreset]
    meta_analysis_source_scoresets: list[ShortScoreset]
    meta_analyses: list[ShortScoreset]
    doi_identifiers: list[SavedDoiIdentifier]
    pubmed_identifiers: list[SavedPubmedIdentifier]
    published_date: Optional[date]
    creation_date: date
    modification_date: date
    created_by: Optional[SavedUser]
    modified_by: Optional[SavedUser]
    target_gene: SavedTargetGene
    dataset_columns: Dict

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Scoreset(SavedScoreset):
    """Score set view model containing most properties visible to non-admin users, but no variant data."""

    experiment: Experiment
    license: License
    superseded_scoreset: Optional[ShortScoreset]
    superseding_scoreset: Optional[Scoreset]
    meta_analysis_source_scoresets: list[ShortScoreset]
    meta_analyses: list[ShortScoreset]
    doi_identifiers: list[DoiIdentifier]
    pubmed_identifiers: list[PubmedIdentifier]
    created_by: Optional[User]
    modified_by: Optional[User]
    target_gene: TargetGene
    num_variants: int
    private: bool
    # processing_state: Optional[str]


class ScoresetWithVariants(Scoreset):
    """
    Score set view model containing a complete set of properties visible to non-admin users, for contexts where variants
    are requested.
    """

    variants: list[VariantInDbBase]


class AdminScoreset(Scoreset):
    """Score set view model containing properties to return to admin clients."""

    normalised: bool
    approved: bool
