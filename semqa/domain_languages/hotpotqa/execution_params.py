from typing import Dict, Optional, List, Any

import torch
import torch.nn
from allennlp.common import Registrable
from allennlp.modules import Seq2SeqEncoder, SimilarityFunction, TextFieldEmbedder, TimeDistributed, FeedForward
from allennlp.modules.similarity_functions.bilinear import BilinearSimilarity
from allennlp.modules.span_extractors import EndpointSpanExtractor
from allennlp.models.reading_comprehension.bidaf import BidirectionalAttentionFlow
from allennlp.modules.matrix_attention.dot_product_matrix_attention import DotProductMatrixAttention
from allennlp.modules.matrix_attention.legacy_matrix_attention import LegacyMatrixAttention
from allennlp.nn import InitializerApplicator, RegularizerApplicator
from allennlp.modules.matrix_attention.matrix_attention import MatrixAttention
from allennlp.models.decomposable_attention import DecomposableAttention
from allennlp.nn.util import masked_softmax, weighted_sum
from semqa.domain_languages.hotpotqa.decompatt import DecompAtt
# from semqa.models.utils.bidaf_utils import PretrainedBidafModelUtils

class ExecutorParameters(torch.nn.Module, Registrable):
    """
    Global parameters for execution. Executor objects are made for each instance, where as these will be shared across.
    """
    def __init__(self,
                 bool_bilinear: SimilarityFunction = None,
                 matrix_attention: MatrixAttention = None,
                 question_token_repr_key: str = None,
                 context_token_repr_key: str = None,
                 decompatt: DecompAtt = None,
                 bidafutils = None,
                 dropout: float = 0.0):
        super(ExecutorParameters, self).__init__()
        # TODO(nitish): Figure out a way to pass this programatically from bidaf
        self._span_extractor = EndpointSpanExtractor(input_dim=200)
        # This can be used to find similarity between two vectors, say question vector and passage vector
        self._bool_bilinear = bool_bilinear
        # This can be used to find the similarity between question tokens and context tokens
        self._matrix_attention = matrix_attention

        self._dotprod_matrixattn = DotProductMatrixAttention()

        self._quescontext_bilinear = BilinearSimilarity(200, 200)

        self._bidafutils = None
        self._question_token_repr_key = question_token_repr_key
        self._context_token_repr_key = context_token_repr_key

        if dropout > 0:
            self._dropout = torch.nn.Dropout(p=dropout)
        else:
            self._dropout = lambda x: x

        # Set this in the model init -- same as the model's text_field_embedder
        self._text_field_embedder: TextFieldEmbedder = None

        self._snli_model: DecomposableAttention = None
        self._decompatt: DecompAtt = decompatt

