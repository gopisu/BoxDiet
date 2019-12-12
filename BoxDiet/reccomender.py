#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turicreate as tc

def prepare_rec():
    actions = tc.SFrame.read_csv('BoxDiet/datasets/dump1.csv')
    items = tc.SFrame.read_csv('BoxDiet/datasets/meals.csv')
    users = tc.SFrame.read_csv('BoxDiet/datasets/users.csv')

    # dealing with missing data
    items = items.dropna(how='any')
    users = users.dropna(how='any')

    # splitting data
    training_data, validation_data = tc.recommender.util.random_split_by_user(actions, 'id', 'meal__id')
    model2 = tc.recommender.ranking_factorization_recommender.create(training_data, user_id='id', item_id='meal__id',
                                                                     target='mark')
    # model training

    return model2, items


def give_reccomendations(user_id, model2, items):
    recommendations = model2.recommend(users=[user_id]).join(right=items, on={'meal__id': 'meal__id'},
                                                             how='inner').sort(['id', 'rank'], ascending=True)
    #create top10 for every user
    recommendations_list = []
    for i in recommendations:
        recommendations_list.append(i)

    return recommendations_list
