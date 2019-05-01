#!/usr/bin/env

SERIALIZATION_DIR='./resources/semqa/checkpoints/drop/num/nc_howmanyyards_count_diff/drop_parser_new/TOKENS_qanet/ED_300/RG_1e-07/QPSIMKEY_enc/SIM_KEY_ma/SUPEPOCHS_5/S_100/pretrain_NoFinetune/'
WEIGHTS_TH=best.th
# WEIGHTS_TH=model_state_epoch_43.th

MODEL_ARCHIVE=${SERIALIZATION_DIR}/model.tar.gz

if [ -f "${MODEL_ARCHIVE}" ]; then
    echo "Model archive exists: ${MODEL_ARCHIVE}"
    exit 1
fi

echo "Making model.tar.gz in ${SERIALIZATION_DIR}"

cd ${SERIALIZATION_DIR}

if [ -d "modeltar" ]; then
    echo "modeltar directory exists. Deleting ... "
    rm -r modeltar
fi


mkdir modeltar
cp -r vocabulary modeltar/
cp ${WEIGHTS_TH} modeltar/weights.th
cp config.json modeltar/
cd modeltar
tar -czvf model.tar.gz ./*
cp model.tar.gz ../
cd ../
rm -r modeltar