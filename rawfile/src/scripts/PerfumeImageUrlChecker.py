import requests as requests


def main():
    from api.src.repository.PerfumeRepository import PerfumeRepository
    lst = list(map(lambda x: (x.idx, x.image_url), PerfumeRepository.get_all_perfume()))
    print("perfume idx list: {}".format(", ".join(map(lambda x: str(x[0]), lst))))
    need_update_list = []
    for perfume_idx, image_url in lst:
        response = requests.get(image_url)
        if response.status_code != 200:
            print("{} : {} -> {}".format(perfume_idx, image_url, response))
            need_update_list.append(perfume_idx)
    print(need_update_list)


if __name__ == '__main__':
    main()