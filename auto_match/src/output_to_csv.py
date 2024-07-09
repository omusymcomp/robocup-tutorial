import csv
import glob

key_word = "(OpponentOffenseCount)"
key_word2 = "(SendOpponentOffensePlayers):"
KEY_WORD3 = "'HELIOS2021'"
opponent_team_flag = False
output_file_path = "../data/output/RoboCup2022_攻撃枚数蓄積システム.csv"

def output_to_csv(add_data_list):
    with open(output_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(add_data_list)


if __name__ == "__main__":
    for_csv = []
    for_csv_tmp = []
    opponent_count_list = []
    #辞書の要素数の最大値は２
    default_offense_opponents = {"CYRUS":[1, 3],"Yushan":[2],"Oxsy":[2],"FRA-UNIted":[-1]}
    result_score = ""
    judge_offense_opponents = ""
    opponent_team = ""

    dataset_path = glob.glob('../data/log_data/*/*.log')
    print("Read Files")
    print(dataset_path)

    for i in dataset_path:
        with open(i) as log_file:
            for f in log_file:
                if f == "\n" or f == "\n\n":
                    continue

                split_with_space = f.split()

                # ex) 1 vs 2
                if opponent_team_flag:
                    result_score = split_with_space[1]+"-"+split_with_space[3]
                    opponent_team_flag = False
                    break

                # ex) (OpponentOffenseCount) 1:476
                if split_with_space[0] == key_word:
                    opponent_count_list.append(split_with_space[1].split(":")[1])
                
                # ex) (SendOpponentOffensePlayers): 3
                if split_with_space[0] == key_word2:
                    judge_offense_opponents = split_with_space[1]

                #ex) 'HELIOS' vs 'CYRUS'
                if split_with_space[0] == KEY_WORD3:
                    opponent_team = split_with_space[2]
                    opponent_team = opponent_team[1:-1]
                    opponent_team_flag = True

        #print(opponent_count_list)
        #print(judge_offense_opponents)
        #print(opponent_team)
        #print(result_score)
        #print("\n")
        try:
            if len(default_offense_opponents[opponent_team]) == 1:
                if default_offense_opponents[opponent_team][0] == int(judge_offense_opponents):
                    answer = "TRUE"
                else:
                    answer = "FALSE"
            else:
                if default_offense_opponents[opponent_team][0] == int(judge_offense_opponents) or default_offense_opponents[opponent_team][1] == int(judge_offense_opponents):
                    answer = "TRUE"
                else:
                    answer = "FALSE"
        except KeyError:
            print("This Team is not registered in dictionary!\nteam name:{}".format(opponent_team))
            answer = ""

        for_csv_tmp.append(opponent_team)
        opponent_team = ""
        for_csv_tmp.append(result_score)
        result_score = ""
        for_csv_tmp.extend(opponent_count_list)
        opponent_count_list = []
        for_csv_tmp.append(judge_offense_opponents)
        judge_offense_opponents = ""
        for_csv_tmp.append(answer)
        answer = ""
        for_csv.append(for_csv_tmp)
        for_csv_tmp = []
        

    #print(for_csv)
    output_to_csv(for_csv)
