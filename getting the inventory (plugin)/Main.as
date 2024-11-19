array<string> structure;

void Main() {
    CGameCtnApp@ app = GetApp();
    CGameCtnEditorCommon@ editor = cast<CGameCtnEditorCommon@>(app.Editor);
    CGameEditorPluginMapMapType@ pmt = editor.PluginMapType;
    CGameEditorGenericInventory@ inventory = pmt.Inventory;

    CGameCtnArticleNodeDirectory@ blocksNode = cast<CGameCtnArticleNodeDirectory@>(inventory.RootNodes[0]);
    ExploreNode(blocksNode);

    string jsonOutput = Json::Write(structure);
    
    IO::File file(IO::FromStorageFolder("InventoryStructure.json"), IO::FileMode::Write);
    file.Write(jsonOutput);
    file.Close();
}

void ExploreNode(CGameCtnArticleNodeDirectory@ parentNode, string _folder = "") {
    for (uint i = 0; i < parentNode.ChildNodes.Length; i++) {
        auto node = parentNode.ChildNodes[i];
        if (node.IsDirectory) {
            structure.InsertLast(_folder + node.Name + "/");
            ExploreNode(cast<CGameCtnArticleNodeDirectory@>(node), _folder + node.Name + "/");
        } else {
            auto ana = cast<CGameCtnArticleNodeArticle@>(node);
            if (ana.Article !is null) {
                auto block = cast<CGameCtnBlockInfo@>(ana.Article.LoadedNod);
                if (block !is null) {
                    structure.InsertLast(_folder + block.Name);
                }
            }
        }
    }
}