#Méthode qui permet de créer les objets qui seront display à l'utilisateur 

def relationship(r_props, r_id, n_id, m_id, center_id, n_name, m_name):
    c = {
        'data': {
            "id": f"{n_id}-{m_id}",
            "props": [r_props],
            "count": 1,
            "source": str(n_id),
            "target": str(m_id),
            "label": '',
            "title": f"Year: {r_props['year_dt']}\nFiling Year: {r_props['filing_year']}\nPatent ID: {r_props['grant_doc_num']}\nPatent Value: {r_props['patent_value']}\nPatent Quality: {r_props['patent_quality']}\nLitigation Risk: {r_props['litigation_risk']}",
            "color": "black",
            "font": "blue",
            "width": 1,
            "mediumPatentValue": r_props['patent_value'],
            "mediumPatentQuality": r_props['patent_quality'],
            "mediumLitigationRisk": r_props['litigation_risk'],
            "n_name": f"{n_name}",
            "m_name": f"{m_name}"

        }
    }


#On a ensuite ce type de méthode qui construit tous les objets à envoyer coté front entilisant d'autres méthodes comme celle montrée au dessus: 
    

def FirmtoJason(results):
    nodes = []
    edges = []



            # Extract the properties of the nodes and relationships
    rKeys = ['year_dt','filing_year', 'patent_value', 'patent_quality', 'litigation_risk', 'grant_doc_num']
    nKeys= ['firm_name','firm_id','firm_country','firm_type']
        # Loop through the query results
    for record in results:

        


        n_props = dict(record["n"])
        m_props = dict(record["m"])
        r_props = dict(record["r"])
        r_id=str(record["r"].id)
        center_id = record['center_id']
        
        m_id=record["m"].id
        n_id=record["n"].id
        node_ids = {}

        #if a field is empty, there will be an error, so we fill each missing field with "unknown"
        for key in nKeys:
            if key not in m_props:
                m_props[key]="unknown"

        for key in nKeys:
            if key not in n_props:
                n_props[key]="unknown"
                
        for key in rKeys:
            if key not in r_props:
                r_props[key] = "unknown"

        for key, value in n_props.items():
            if not value:
                n_props[key] = "unknown"
        for key, value in m_props.items():
            if not value:
                m_props[key] = "unknown"
        for key, value in r_props.items():
            if not value:
                r_props[key] = "unknown"

        #We make sure that each node is only present ONCE, or there will be an error
        nodes_ids = set([e["data"]["id"] for e in nodes])
        a = firm(n_props, n_id, 1)
        b = firm(m_props, m_id, 2)

        if a["data"]["id"] not in nodes_ids:
            nodes.append(a)
            nodes_ids.add(a["data"]["id"])  # Add new ID to the set

        if b["data"]["id"] not in nodes_ids:
            nodes.append(b)
            nodes_ids.add(b["data"]["id"]) #  Save this node to the dictionary

        
        c = relationship(r_props, r_id, n_id, m_id, center_id, n_props["firm_name"],m_props["firm_name"])
        edge_ids = {e["data"]["id"]: e for e in edges}
       


        #The key of the edge will be depending on the two nodes it connects
        #So that of two edges connect two 2 edges in the same direction they will have the same key

        edge_key = f"{n_id}-{m_id}"
        #If the key is already existing, we aggregate the two edges together, and we add to the width 
        edge_ids = {e["data"]["id"]: e for e in edges}
        if edge_key in edge_ids:
                edge_ids[edge_key]["data"]["title"] += f"\n-----\nYear: {r_props['year_dt']}\nPatent ID: {r_props['grant_doc_num']}\nFiling Year: {r_props['filing_year']}\nPatent Value: {r_props['patent_value']}\nPatent Quality: {r_props['patent_quality']}\nLitigation Risk: {r_props['litigation_risk']}"
                edge_ids[edge_key]["data"]["count"] += 1
                edge_ids[edge_key]["data"]["width"] = 1+log(edge_ids[edge_key]["data"]["count"])
                edge_ids[edge_key]["data"]["label"] = str(edge_ids[edge_key]["data"]["count"])
                non_center_id = n_id if m_id == center_id else m_id
                non_center_nodes = [node for node in nodes if node['data']['id'] == str(non_center_id)]
                if non_center_nodes:
                    non_center_node = non_center_nodes[0]
                    non_center_node["data"]["count"] += 1
                    non_center_node["data"]["size"] = int(30 + 2*(10 * log(non_center_node["data"]["count"])))
                if edge_ids[edge_key]["data"]["mediumPatentValue"] == 'unknown':
                    if r_props['patent_value'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumPatentValue"] = float(r_props['patent_value'])
                else:
                    if r_props['patent_value'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumPatentValue"] = round((edge_ids[edge_key]["data"]["mediumPatentValue"] * (edge_ids[edge_key]["data"]["count"] - 1) + float(r_props['patent_value'])) / edge_ids[edge_key]["data"]["count"], 2)

                # For mediumPatentQuality
                if edge_ids[edge_key]["data"]["mediumPatentQuality"] == 'unknown':
                    if r_props['patent_quality'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumPatentQuality"] = float(r_props['patent_quality'])
                else:
                    if r_props['patent_quality'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumPatentQuality"] = round((edge_ids[edge_key]["data"]["mediumPatentQuality"] * (edge_ids[edge_key]["data"]["count"] - 1) + float(r_props['patent_quality'])) / edge_ids[edge_key]["data"]["count"], 2)

                # For mediumLitigationRisk
                if edge_ids[edge_key]["data"]["mediumLitigationRisk"] == 'unknown':
                    if r_props['litigation_risk'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumLitigationRisk"] = float(r_props['litigation_risk'])
                else:
                    if r_props['litigation_risk'] != 'unknown':
                        edge_ids[edge_key]["data"]["mediumLitigationRisk"] = round((edge_ids[edge_key]["data"]["mediumLitigationRisk"] * (edge_ids[edge_key]["data"]["count"] - 1) + float(r_props['litigation_risk'])) / edge_ids[edge_key]["data"]["count"], 2)
                
                
        else:
            if a["data"]["id"] in nodes_ids and b["data"]["id"] in nodes_ids:
                edges.append(c)
                
    for edge in edges:
        edge["data"]["title"] = f"Total Transactions: {edge['data']['count']}\n Average Patent Value: {edge['data']['mediumPatentValue']}\nAverage Patent Quality: {edge['data']['mediumPatentQuality']}\nAverage Litigation Risk: {edge['data']['mediumLitigationRisk']}\n\nList of transactions:" + edge["data"]["title"]

    return nodes, edges