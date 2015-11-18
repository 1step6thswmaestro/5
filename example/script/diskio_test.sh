sysbench --num-threads=1 --file-block-size=65536 --file-num=2 --file-test-mode=seqwr --test=fileio run
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"
sysbench --num-threads=1 --file-block-size=65536 --file-num=2 --file-test-mode=seqrd --test=fileio run

