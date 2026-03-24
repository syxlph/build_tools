import os


def find_local_sdkjs_plugins(workspace_root):
    plugins_root = os.path.join(workspace_root, "sdkjs-plugins")
    if not os.path.isdir(plugins_root):
        return []

    plugins = []
    for entry in sorted(os.listdir(plugins_root)):
        config_path = os.path.join(plugins_root, entry, "config.json")
        if os.path.isfile(config_path):
            plugins.append(entry)

    return plugins


def copy_local_sdkjs_plugins(
    workspace_root,
    dst_dir,
    base_module,
    is_name_as_guid=False,
    is_desktop_local=False,
):
    plugins_root = os.path.join(workspace_root, "sdkjs-plugins")
    plugins = find_local_sdkjs_plugins(workspace_root)

    for plugin_name in plugins:
        base_module.copy_sdkjs_plugin(
            plugins_root,
            dst_dir,
            plugin_name,
            is_name_as_guid=is_name_as_guid,
            is_desktop_local=is_desktop_local,
        )

    return plugins
