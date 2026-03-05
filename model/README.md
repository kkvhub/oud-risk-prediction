# model/

Place the following three artefacts here after training:

| File                    | Description                                                              |
|-------------------------|--------------------------------------------------------------------------|
| `final_nn.keras`        | Trained Keras neural-network model (SavedModel / `.keras` format)        |
| `preprocessor.pkl`      | Fitted scikit-learn `ColumnTransformer` or `Pipeline` used during training |
| `optimal_thresholds.pkl`| `dict` mapping class index (int) → optimal probability threshold (float) |

These files are **not** committed to version control because they are large binary artefacts.
Generate them by running your training notebook / script and copying the outputs here.
