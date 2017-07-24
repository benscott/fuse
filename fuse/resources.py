#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '29/01/2017'.

Override default resource behaviour

"""

import random
from flask import request, jsonify

from fuse.api.schema import Schema
from fuse.api.resource import APIResource, RecordAPIResource, ListAPIResource, SchemaAPIResource
from fuse.api.collection import Collection


class CustomAPIResource(APIResource):

    def get(self):
        """
        Get one record that has not yet been transcribed
        :return:
         ---
         description: List {slug} records
         ---
        """

        # Prevent multiple people working on same doc
        limit = 10
        skip = random.randint(1, limit)

        # Query MongoDB - gets result cursor
        record = Collection(self.slug).find({'country': {'$exists': None}}).limit(limit).skip(skip)

        # Return JSON dict of records and total
        # Explicity pass through jsonify so it uses custom JSONEncoder
        return jsonify({
            'total': 1 if record else 0,
            'schema': Schema().load(self.slug),
            'record': record[0]
        })