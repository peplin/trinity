import neo4j
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers.base import BaseHandler

class RelationshipHandler(BaseHandler):
    @neo4j.transactional(BaseHandler.graph)
    def post(self, node_id):
        typ = self.get_json_argument('link_type')
        to = self.get_json_argument('to')
        data = self.get_json_argument('data', {})
        append = self.get_json_argument('append', False)

        node = self.find_node(node_id)
        to_node = self.find_node(to)
        
        relationship = None
        if append:
            for existing_relationship in getattr(node, typ):
                if existing_relationship.getOtherNode(node) == to_node:
                    relationship = existing_relationship.update(**data)
                    break
        if not relationship:
            relationship = getattr(node, typ)(to_node, **data)
        self.write({'from_node': node_id,
                'to': to,
                'link_type': typ,
                'data': dict(relationship.items())})
