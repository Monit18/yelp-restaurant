 #from py2neo import Graph
 #import config
 #
 #uri = "{}://{}:{}@{}:{}".format(config.PROTO, config.USER, config.PASSWORD, config.HOSTNAME, config.PORT)
 #
 #graph = Graph(uri)
#graph = Graph(scheme="bolt", host="localhost",port=8001, auth=('neo4j', '1532'))

import os
from py2neo import Graph
import config
graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)

print("[INFO] Clearing graph of any existing data")
graph.evaluate("MATCH (n) DETACH DELETE n")

print("[INFO] Asserting schema")
graph.evaluate("CALL apoc.schema.assert({Category:['name']},{Business:['id'],User:['id'],Review:['id']})")

print("[INFO] Loading businesses")
graph.evaluate('CALL apoc.periodic.iterate("'
        'CALL apoc.load.json(\'file:///yelp/yelpsubset/business_subset_001.json\') YIELD value RETURN value '
               '"," '
               'MERGE (b:Business{id:value.business_id}) '
               'SET b += apoc.map.clean(value, [\'business_id\',\'categories\',\'postal_code\'],[]) '
               'WITH b,value.categories as categories '
               'UNWIND categories as category '
               'MERGE (c:Category{id:category}) '
               'MERGE (b)-[:IN_CATEGORY]->(c)"'
               ',{batchSize: 10000, iterateList: true});')

 #print("[INFO] Loading users")
 #graph.evaluate('CALL apoc.periodic.iterate("'
 #               'CALL apoc.load.json(\'file:///user.json\') '
 #               'YIELD value RETURN value '
 #               '"," '
 #               'MERGE (u:User{id:value.user_id}) '
 #               'SET u += apoc.map.clean(value, [\'friends\',\'user_id\'],[0]) '
 #               'WITH u,value.friends as friends '
 #               'UNWIND friends as friend '
 #               'MERGE (u1:User{id:friend}) '
 #               'MERGE (u)-[:FRIEND]-(u1) '
 #               '",{batchSize: 100, iterateList: true});')
 #
 #print("[INFO] Loading reviews")
 #graph.evaluate('CALL apoc.periodic.iterate("'
 #               'CALL apoc.load.json(\'file:///review.json\') '
 #               'YIELD value RETURN value '
 #               '"," '
 #               'MERGE (b:Business{id:value.business_id}) '
 #               'MERGE (u:User{id:value.user_id}) '
 #               'MERGE (u)-[r:REVIEWS]->(b) '
 #               'SET r += apoc.map.clean(value, [\'business_id\',\'user_id\',\'review_id\'],[0])'
 #               '",{batchSize: 10000, iterateList: true});')
