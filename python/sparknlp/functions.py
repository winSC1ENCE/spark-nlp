from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql import DataFrame
import sys
import sparknlp


def map_annotations_udf(f, output_type: DataType):
    sys.modules['sparknlp.annotation'] = sparknlp  # Makes Annotation() pickle serializable  in top-level
    return udf(
        lambda content: f(content),
        output_type
    )


def map_annotations_to_annotations_udf(f, output_type: DataType):
    from sparknlp.annotation import Annotation
    sys.modules['sparknlp.annotation'] = sparknlp  # Makes Annotation() pickle serializable in top-level
    return udf(
        lambda content: f(content),
        ArrayType(Annotation.dataType())
    )


def map_annotations(dataframe: DataFrame, f, column, output_column, output_type):
    dataframe.withColumn(output_column, map_annotations_udf(f, output_type)(column))


def filter_by_annotations(dataframe, f, column):
    this_udf = udf(
        lambda content: f(content),
        BooleanType()
    )
    return dataframe.filter(this_udf(column))


def explode_annotations(dataframe: DataFrame, column, output_column):
    from pyspark.sql.functions import explode
    return dataframe.withColumn(output_column, explode(column))
