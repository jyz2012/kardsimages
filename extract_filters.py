import os
import json

def main():
    jsons_dir = "jsons"
    output_file = "filters.json"
    
    all_filters = []
    
    # 遍历jsons文件夹
    for filename in os.listdir(jsons_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(jsons_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取cards.edges数组
                if 'data' in data and 'cards' in data['data'] and 'edges' in data['data']['cards']:
                    edges = data['data']['cards']['edges']
                    
                    for edge in edges:
                        if 'node' in edge and 'json' in edge['node']:
                            node_json = edge['node']['json']
                            node = edge['node']
                            
                            # 提取需要的字段
                            card_data = {
                                'id': node_json.get('id'),
                                'faction': node_json.get('faction'),
                                'kredits': node_json.get('kredits'),
                                'imageUrl': node.get('imageUrl')
                            }
                            
                            all_filters.append(card_data)
                            
                print(f"处理完成: {filename}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")
    
    # 写入filters.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_filters, f, ensure_ascii=False, indent=2)
    
    print(f"完成！共提取 {len(all_filters)} 条记录到 {output_file}")

if __name__ == "__main__":
    main()
