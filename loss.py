import torch
import torch.nn as nn
import torch.nn.functional as F


def cosine_distance(context, answer):
    """
    Args:
        x: tensor of shape [batch_size, emb_size]
        y: tensor of shape [batch_size, emb_size]
    Returns:
        cos_dists: tensor of shape [batch_size, batch_size]
    """

    context = context.div(context.norm(p=2, dim=1, keepdim=True))
    answer = answer.div(answer.norm(p=2, dim=1, keepdim=True))

    distances = torch.sub(1, torch.mm(context, answer.transpose(1, 0)))
    distances = torch.clamp_min(distances, 1e-8)

    return distances


def batch_all_sampler(distances):

    batch_size = distances.shape[0]

    label_equal = torch.diagflat(torch.ones(batch_size)).byte()
    i_equal_j = label_equal.unsqueeze(2)
    i_equal_k = label_equal.unsqueeze(1)

    i_notequal_k = ~i_equal_k
    mask = i_equal_j & i_notequal_k

    return mask.float()


def triplet_loss(context_embeddings, answer_embeddings, margin=0.05):

    cos_dists = cosine_distance(context_embeddings, answer_embeddings)
    mask = batch_all_sampler(cos_dists)

    anchor_positive_dist = cos_dists.unsqueeze(2)
    anchor_negative_dist = cos_dists.unsqueeze(1)
    triplet_loss = F.relu(anchor_positive_dist - anchor_negative_dist + margin)
    triplet_loss = triplet_loss * mask

    num_positive_triplets = torch.gt(triplet_loss, 1e-16).sum()
    triplet_loss = triplet_loss.sum() / (num_positive_triplets + 1e-16)

    return triplet_loss


def margin_loss(context_embeddings, answer_embeddings, beta=0.4, margin=0.1):
    pass


def contrastive_loss(context_embeddings, answer_embeddings):
    pass


def sample(distances, strategy='all'):
    # all, hard, weighted
    anchor, positive, negative = None, None, None

    return anchor, positive, negative
