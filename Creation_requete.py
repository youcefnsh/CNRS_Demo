
#Voilà un exemple d'une des méthodes qui transforme les inputs des utilisateurs en une requete Sypher.


def generate_cypher_query(data):
    params = {}
    center_firm_name = data.get('center_firm_name')
    params["center_firm_name"] = center_firm_name

    query = """MATCH (center:Firm)
               WHERE toLower(center.firm_name) = toLower($center_firm_name)
               MATCH (center)-[r:Transaction]-(other:Firm)
               WHERE 1=1 """

    query += """WITH center, r, other,
                       CASE
                           WHEN startNode(r) = center THEN {n: center, m: other}
                           ELSE {n: other, m: center}
                       END as nm_info
                WHERE 1=1"""

    property_map = {
        'seller_name': ('toLower(nm_info.n.firm_name)', 'str'),
        'seller_type': ('toLower(nm_info.n.firm_type)', 'str'),
        'seller_country': ('toLower(nm_info.n.firm_country)', 'str'),
        'buyer_name': ('toLower(nm_info.m.firm_name)', 'str'),
        'buyer_type': ('toLower(nm_info.m.firm_type)', 'str'),
        'buyer_country': ('toLower(nm_info.m.firm_country)', 'str'),
        'transaction_year_start': ('r.year_dt', 'int'),
        'transaction_year_end': ('r.year_dt', 'int'),
        'lower_patent_value': ('r.patent_value', 'int'),
        'upper_patent_value': ('r.patent_value', 'int'),
        'lower_litigation_risk': ('r.litigation_risk', 'int'),
        'upper_litigation_risk': ('r.litigation_risk', 'int'),
    }

    for key, value in data.items():
        if value and key not in ('limit', 'center_firm_name'):
            params[key] = value
            prop, prop_type = property_map[key]
            if prop_type == 'str':
                if key in ('seller_name', 'seller_type', 'seller_country'):
                    query += f" AND (nm_info.n = center OR {prop} = toLower(${key}))"
                else: 
                    query += f" AND (nm_info.m = center OR {prop} = toLower(${key}))"
            elif prop_type == 'int':
                if key == 'transaction_year_start':
                    query += f" AND {prop} >= ${key}"
                elif key == 'transaction_year_end':
                    query += f" AND {prop} <= ${key}"
                elif key == 'lower_patent_value':
                    query += f" AND {prop} >= ${key}"
                elif key == 'upper_patent_value':
                    query += f" AND {prop} <= ${key}"
                elif key == 'lower_litigation_risk':
                    query += f" AND {prop} >= ${key}"
                elif key == 'upper_litigation_risk':
                    query += f" AND {prop} <= ${key}"

    if data.get('limit'):
        params["limit"] = data.get('limit')
        query += " RETURN nm_info.n AS n, r, nm_info.m AS m, id(center) as center_id LIMIT $limit"
    else:
        query += " RETURN nm_info.n AS n, r, nm_info.m AS m, id(center) as center_id"
    
    return query, params