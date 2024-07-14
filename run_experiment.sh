databaseName=$1

for nodesCount in 5 10 15 20 25; do
    for numFriends in 2 4 6; do

        for graphIndex in {1..10}; do

            randomSeed=$((1 + $RANDOM % 1000000))

            date
            echo "Running with $((nodesCount)) nodes and $numFriends firends"
            echo "Random seed: $randomSeed"
            
            python3 run_algorithms_1_and_2.py random_algorithm_2_plus twitter $((nodesCount)) $numFriends $graphIndex $randomSeed fpt randomAlgo 2
            python3 run_algorithms_1_and_2.py random_algorithm_3_plus twitter $((nodesCount)) $numFriends $graphIndex $randomSeed new_fpt3 randomAlgo 3
            
        done
    done
done