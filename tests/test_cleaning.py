import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from src.transformations.cleaning import (
    drop_high_null_columns,
    replace_interrogation_marks,
    remove_invalid_gender,
    create_readmission_flag,
    clean,
)


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()


@pytest.fixture
def sample_df(spark):
    schema = StructType([
        StructField("encounter_id", IntegerType()),
        StructField("gender", StringType()),
        StructField("race", StringType()),
        StructField("weight", StringType()),
        StructField("payer_code", StringType()),
        StructField("medical_specialty", StringType()),
        StructField("diag_1", StringType()),
        StructField("diag_2", StringType()),
        StructField("diag_3", StringType()),
        StructField("time_in_hospital", IntegerType()),
        StructField("readmitted", StringType()),
    ])
    data = [
        (1, "Male", "?", "?", "SP", "Cardiology", "250", "401", "?", 3, "<30"),
        (2, "Female", "Caucasian", "?", "?", "?", "?", "250", "250", 5, ">30"),
        (3, "Unknown/Invalid", "Asian", "75", "MC", "Internal", "250", "250", "250", 1, "NO"),
    ]
    return spark.createDataFrame(data, schema)


def test_drop_high_null_columns(sample_df):
    result = drop_high_null_columns(sample_df)
    assert "weight" not in result.columns
    assert "payer_code" not in result.columns


def test_replace_interrogation_marks(sample_df):
    result = replace_interrogation_marks(sample_df)
    invalid = result.filter(result.race == "?").count()
    assert invalid == 0


def test_remove_invalid_gender(sample_df):
    result = remove_invalid_gender(sample_df)
    assert result.count() == 2


def test_create_readmission_flag(sample_df):
    result = create_readmission_flag(sample_df)
    assert "readmitted_flag" in result.columns
    flags = [row.readmitted_flag for row in result.collect()]
    assert flags == [1, 0, 0]


def test_clean_pipeline(sample_df):
    result = clean(sample_df)
    assert "weight" not in result.columns
    assert result.count() == 2
    assert "readmitted_flag" in result.columns