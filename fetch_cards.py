import requests
import json
import os

def main():
    url = "https://herokuapi.kards.com/graphql"
    
    base_query = """query getCards($language: String, $offset: Int, $nationIds: [Int], $kredits: [Int], $q: String, $type: [String], $rarity: [String], $set: [String], $showSpawnables: Boolean, $showExiles: Boolean, $showReserved: Boolean) {
  cards(
    language: $language
    first: 20
    offset: $offset
    nationIds: $nationIds
    kredits: $kredits
    q: $q
    type: $type
    set: $set
    rarity: $rarity
    showSpawnables: $showSpawnables
    showExiles: $showExiles
    showReserved: $showReserved
  ) {
    pageInfo {
      count
      hasNextPage
      __typename
    }
    edges {
      node {
        id
        cardId
        importId
        json
        reserved
        imageUrl: image(language: $language)
        thumbUrl: image(type: thumb, language: $language)
        __typename
      }
      __typename
    }
    __typename
  }
}"""
    
    os.makedirs("jsons", exist_ok=True)
    
    offset = 0
    request_count = 1
    
    while offset <= 1600:
        payload = {
            "operationName": "getCards",
            "variables": {
                "offset": offset,
                "language": "zh",
                "showSpawnables": True,
                "showExiles": False,
                "showReserved": True
            },
            "query": base_query
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            with open(f"jsons/{request_count}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"已保存第 {request_count} 次请求的结果 (offset: {offset})")
            
            offset += 20
            request_count += 1
        except Exception as e:
            print(f"请求失败: {e}")
            break

if __name__ == "__main__":
    main()
