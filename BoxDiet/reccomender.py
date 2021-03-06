#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turicreate as tc
from psycopg2 import connect


def prepare_rec():
    cnx = connect(
        user="postgres", password="coderslab", host="localhost", database="BoxDiet1"
    )

    actions = tc.SFrame.from_sql(
        cnx, 'SELECT meal_id, user_id, mark FROM "BoxDiet_rank"'
    )
    items = tc.SFrame.from_sql(cnx, 'SELECT * FROM "BoxDiet_meal"')
    cnx.close()
    # dealing with missing data
    items = items.dropna(how="any")

    # splitting data is not necessary here
    # training_data, validation_data = tc.recommender.util.random_split_by_user(actions, 'user_id', 'meal_id')
    # model training
    model2 = tc.recommender.ranking_factorization_recommender.create(
        actions, user_id="user_id", item_id="meal_id", target="mark"
    )

    return model2, items


def give_reccomendations(user_id, model2, items):
    recommendations = (
        model2.recommend(users=[user_id])
            .join(right=items, on={"meal_id": "meal_id"}, how="inner")
            .sort(["user_id", "rank"], ascending=True)
    )
    # create top10 for every user
    recommendations_list = []
    for i in recommendations:
        recommendations_list.append(i)

    return recommendations_list


def predict(user_id, meal_id):
    my_model = tc.load_model("my_model_file")
    prediction = my_model.predict(dataset={"id": user_id, "meal__id": meal_id})
    dict = {}
    for item in prediction:
        dict["prediction"] = item
    dict["user_id"] = str(user_id)
    dict["meal_id"] = str(meal_id)
    return dict
