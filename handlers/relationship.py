import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

import logging
logger = logging.getLogger('trinity.' + __name__)


class RelationshipHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def post(self, node_id):
        typ = self.get_json_argument('link_type')
        to = self.get_json_argument('to')
        data = self.get_json_argument('data', {})
        append = self.get_json_argument('append', False)
        increment_attributes = self.get_json_argument('increment', [])

        node = self.find_node_or_404(node_id)
        to_node = self.find_node_or_404(to)

        if node == to_node:
            msg = ("Start (%s) and end node (%s) can't be the same"
                    % (node, to_node))
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

        relationship = None
        for existing_relationship in getattr(node, typ):
            if existing_relationship.getOtherNode(node) == to_node:
                relationship = existing_relationship

        if relationship is None:
            relationship = getattr(node, typ)(to_node, **data)
            logger.debug("Created new relationship %s with attached data %s"
                    % (relationship, data))
        else:
            logger.debug("Found existing relationship %s with "
                    " -- not creating another" % relationship)

        if append:
            for existing_relationship in getattr(node, typ):
                if existing_relationship.getOtherNode(node) == to_node:
                    relationship = existing_relationship.update(**data)
                    logger.debug("Updated existing relationship %s to include "
                            "%s" % (relationship, data))
                    break

        for increment_attribute in increment_attributes:
            original = relationship.get(increment_attribute, 0)
            try:
                # LH #30 - handle JPype objects that bubble up
                # TODO try without this...see if our encoder works
                relationship[increment_attribute] = int(unicode(original)) + 1
            except TypeError:
                msg = ("Existing attribute (%s = %s) is not incrementable"
                        % (increment_attribute, original))
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            else:
                logger.debug("Incremented %s attribute on %s to %s"
                        % (increment_attribute, relationship,
                            relationship[increment_attribute]))
        self.write({'from_node': node_id,
                'to': to,
                'link_type': typ,
                'data': dict(relationship.items())})
