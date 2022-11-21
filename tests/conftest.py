# SPDX-FileCopyrightText: Copyright DB Netz AG and the rm-bridge contributors
# SPDX-License-Identifier: Apache-2.0

import pathlib
import typing as t

import pytest
from capellambse import MelodyModel, decl

from rm_bridge import load
from rm_bridge.changeset import actiontypes as act

TEST_DATA_PATH = pathlib.Path(__file__).parent / "data"
TEST_CONFIG = t.cast(
    act.Config, load.load_yaml(TEST_DATA_PATH / "config.yaml")
)
TEST_MODEL_PATH = TEST_DATA_PATH / TEST_CONFIG["model"]["path"]
TEST_MOD_CHANGESET_PATH = TEST_DATA_PATH / "changesets" / "mod.yaml"
TEST_REQ_MODULE_UUID = "3be8d0fc-c693-4b9b-8fa1-d59a9eec6ea4"
TEST_UUID_PREFIX = "00000000-0000-0000-0000-00000000000"


@pytest.fixture
def migration_model() -> MelodyModel:
    return MelodyModel(path=TEST_MODEL_PATH)


@pytest.fixture
def clean_model() -> MelodyModel:
    model = MelodyModel(path=TEST_MODEL_PATH)
    reqmodule = model.by_uuid(TEST_REQ_MODULE_UUID)
    del reqmodule.requirement_types_folders[0]
    del reqmodule.folders[0]
    return model


@pytest.fixture
def deletion_model(migration_model: MelodyModel) -> MelodyModel:
    decl.apply(migration_model, TEST_MOD_CHANGESET_PATH)
    return migration_model
