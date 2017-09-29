#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '29/01/2017'.

Override default resource behaviour

"""

import random
import pymongo
from flask import request, jsonify

from fuse.api.schema import Schema
from fuse.api.resource import APIResource, RecordAPIResource, ListAPIResource, SchemaAPIResource
from fuse.api.collection import Collection
from fuse.api.document import Document


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
        record = Collection(self.slug).find().sort('transcription_count', pymongo.DESCENDING).limit(limit).skip(skip)

        # Return JSON dict of records and total
        # Explicity pass through jsonify so it uses custom JSONEncoder
        return jsonify({
            'total': 1 if record else 0,
            'schema': Schema().load(self.slug),
            'record': record[0]
        })

    def put(self, identifier):
        """
        :param identifier:
        :return:
         ---
         description: Updates a {slug} record
         ---
        """
        data = request.get_json()

        # Create transcription
        Document('transcription').create(data)

        doc = Document('specimen')
        specimen = doc.read(identifier)

        specimen.setdefault('transcription_count', 0)
        specimen['transcription_count'] += 1

        update_result = doc.update(identifier, specimen)
        # # Mongo 2.x does not return an update_result.modified_count - even though record is updated
        # # This is breaking travis build, so we'll just check a document's been matched
        if update_result.matched_count == 1:
            return self.success(message="Record updated")
        else:
            return self.fail(message="Record not updated")
