import os
import yaml
from pyecharts.charts import Map
from pyecharts import options as opts


def load_travel_config(config_path="travel_config.yml"):
    """加载旅行配置文件."""
    with open(config_path, 'r', encoding='utf-8') as ymlfile:
        return yaml.safe_load(ymlfile)


def generate_china_map(province_city_dict, output_path="全国.html"):
    """生成全国足迹地图."""
    province_dict = dict(zip(province_city_dict.keys(), [1] * len(province_city_dict.keys())))

    map = Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
    map.set_global_opts(
        title_opts=opts.TitleOpts(title="个人足迹地图"),
        visualmap_opts=opts.VisualMapOpts(
            max_=1,
            is_piecewise=True,
            pieces=[
                {"max": 1, "min": 1, "label": "去过", "color": "#4EA397"}
            ]
        )
    )
    map.add("个人足迹地图", data_pair=list(province_dict.items()), maptype="china", is_roam=True)
    map.render(output_path)
    print(f"全国足迹地图生成成功: {output_path}")


def generate_province_maps(province_city_dict, output_dir="provinces"):
    """生成各省足迹地图。"""
    os.makedirs(output_dir, exist_ok=True)

    for province, cities in province_city_dict.items():
        # 判断城市列表是否为空，若为空则跳过该省份的地图生成
        if not cities:
            print(f"省份 {province} 的城市列表为空，跳过该省份的地图生成。")
            continue

        map = Map(init_opts=opts.InitOpts(width='1200px', height='800px'))
        map.set_global_opts(
            title_opts=opts.TitleOpts(title=f"个人足迹地图-{province}"),
            visualmap_opts=opts.VisualMapOpts(
                max_=1,
                is_piecewise=True,
                pieces=[{
                    "max": 1, "min": 1, "label": "去过", "color": "#4EA397"},
                    {"max": 0, "min": 0, "label": "未去过", "color": "#FFFFFF"},
                ]
            )
        )
        # 使用城市列表创建字典，默认值为 1
        city_dict = dict(zip(cities, [1] * len(cities)))
        map.add(f"个人足迹地图-{province}", data_pair=list(city_dict.items()), maptype=province, is_roam=True)
        output_path = os.path.join(output_dir, f"{province}.html")
        map.render(output_path)
        #add_centering_style(output_path)  # 添加居中样式
        print(f"生成个人足迹地图-{province} 成功: {output_path}")



def main():
    config_path = "travel_config.yml"
    province_city_dict = load_travel_config(config_path)
    # 生成各省地图
    generate_province_maps(province_city_dict)

    # 生成全国地图
    generate_china_map(province_city_dict)


if __name__ == "__main__":
    main()
