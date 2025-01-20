cd /workspaces
mkdir app
cp /workspaces/zmk-config/config/west.yml /workspaces/app/
west init -l app/
#west update
#git apply --ignore-whitespace /patches/*.patch
#west zephyr-export

#rm -r build
#west build  -d "build/corne36_tball1" -s zmk/app -b "seeeduino_xiao_ble" -- -DZMK_CONFIG=/workspaces/zmk-config/config/ -DSHIELD="corne36_tball1"        
#mkdir zmk-config/release
#mkdir zmk-config/release/corne36_tball1
#cp "build/corne36_tball1/zephyr/zmk.uf2"  zmk-config/release/corne36_tball1/corne36_tball1.uf2