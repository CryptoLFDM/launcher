# This Python file uses the following encoding: utf-8
from jinja2 import Template
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt, QFile, QIODevice, QTextStream

template_jinja = '''
# Global tags can be specified here in key="value" format.
[global_tags]
    {% if launcher_id is defined  and lancher_id | length > 1 %}
    launcher_id = "{{ launcher_id }}"
    {% endif %}
    {% if name is defined and name | length > 1 %}
    name = "{{ name }}"
    {% endif %}

# Configuration for telegraf agent
[agent]
    interval = "60s"
    round_interval = true
    metric_batch_size = 1000
    metric_buffer_limit = 10000
    collection_jitter = "0s"
    flush_interval = "10s"
    flush_jitter = "0s"
    debug = false
    quiet = false

{% if logfile_enabled %}
  logtarget = "file"
  logfile = "{{ telegraf_log_file_path }}"
  logfile_rotation_interval = "1d"
  logfile_rotation_max_size = "100MB"
  logfile_rotation_max_archives = 1
{% endif %}

  hostname = ""
  omit_hostname = false


###############################################################################
#                            OUTPUT PLUGINS                                   #
###############################################################################

# Configuration for Elasticsearch to send metrics to.
[[outputs.elasticsearch]]
    urls = {{ es_host_list }}
    timeout = "5s"
    enable_sniffer = false
    health_check_interval = "10s"
    username = "{{ es_username }}"
    password = "{{ es_password }}"
    index_name = "data-{{ es_username }}"
    tls_ca = "ether-source.pem"
    insecure_skip_verify = true
    manage_template = true
    template_name = "data"
    overwrite_template = false

###############################################################################
#                            INPUT PLUGINS                                    #
###############################################################################

{% if os_is_windows %}
[[inputs.win_perf_counters]]
    [[inputs.win_perf_counters.object]]
        ObjectName = "Processor"
        Instances = ["*"]
        Counters = [
          "% Idle Time",
          "% Interrupt Time",
          "% Privileged Time",
          "% User Time",
          "% Processor Time",
          "% DPC Time",
        ]
        Measurement = "win_cpu"
        IncludeTotal=true

    [[inputs.win_perf_counters.object]]
        ObjectName = "Process"
        Counters = [
            "% Processor Time",
            "Handle Count",
            "Private Bytes",
            "Thread Count",
            "Virtual Bytes",
            "Working Set"
        ]
        Instances = {{ process_list_to_harvest }}
        Measurement = "win_proc"

    [[inputs.win_perf_counters.object]]
        ObjectName = "LogicalDisk"
        Instances = ["*"]
        Counters = [
          "% Idle Time",
          "% Disk Time",
          "% Disk Read Time",
          "% Disk Write Time",
          "% Free Space",
          "Free Megabytes",
        ]
        Measurement = "win_disk"
        IncludeTotal= true

    [[inputs.win_perf_counters.object]]
        ObjectName = "PhysicalDisk"
        Instances = ["*"]
        Counters = [
          "Disk Read Bytes/sec",
          "Disk Write Bytes/sec",
          "Current Disk Queue Length",
          "Disk Reads/sec",
          "Disk Writes/sec",
          "% Disk Time",
          "% Disk Read Time",
          "% Disk Write Time",
          "Temperature",
        ]
        Measurement = "win_diskio"

    [[inputs.win_perf_counters.object]]
        ObjectName = "Network Interface"
        Instances = ["*"]
        Counters = [
          "Bytes Received/sec",
          "Bytes Sent/sec",
          "Packets Received/sec",
          "Packets Sent/sec",
          "Packets Received Discarded",
          "Packets Outbound Discarded",
          "Packets Received Errors",
          "Packets Outbound Errors",
        ]
        Measurement = "win_net"

    [[inputs.win_perf_counters.object]]
        ObjectName = "System"
        Counters = [
          "Context Switches/sec",
          "System Calls/sec",
          "Processor Queue Length",
          "System Up Time",
        ]
        Instances = ["------"]
        Measurement = "win_system"

    [[inputs.win_perf_counters.object]]
        ObjectName = "Memory"
        Counters = [
          "Available Bytes",
          "Cache Faults/sec",
          "Demand Zero Faults/sec",
          "Page Faults/sec",
          "Pages/sec",
          "Transition Faults/sec",
          "Pool Nonpaged Bytes",
          "Pool Paged Bytes",
          "Standby Cache Reserve Bytes",
          "Standby Cache Normal Priority Bytes",
          "Standby Cache Core Bytes",
        ]
        Instances = ["------"]
        Measurement = "win_mem"

    [[inputs.win_perf_counters.object]]
        ObjectName = "Paging File"
        Counters = [
            "% Usage",
        ]
        Instances = ["_Total"]
        Measurement = "win_swap"
{% endif %}

{% if nvidia_smi_enabled %}
[[inputs.nvidia_smi]]
    interval = "10s"
    bin_path = "{{ nvidia_smi_bin_path }}"
{% endif %}

{% if chia_collect_info_enabled %}
[[inputs.http]]
    name_override = "http-chia"
    urls = [
        "https://localhost:8560/get_plots"
    ]
    method = "POST"
    headers = {"Content-Type" = "application/json"}
    body = "{}"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    data_format = "json"
    json_query = "plots"
    json_string_fields = [
                        "filename",
                        "plot-seed",
                        "plot_id",
                        "plot_public_key",
                        "pool_contract_puzzle_hash",
                        "pool_public_key"
                        ]
    tagexclude = ["url"]

[[inputs.http]]
    name_override = "http-chia"
    urls = [
        "https://localhost:8555/get_blockchain_state"
    ]
    method = "POST"
    headers = {"Content-Type" = "application/json"}
    body = "{}"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    json_query = "blockchain_state.sync"
    data_format = "json"
    json_string_fields = ["synced"]
    tagexclude = ["url"]

[[inputs.http]]
    name_override = "http-chia"
    urls = [
            "https://localhost:9256/get_sync_status",
    ]
    method = "POST"
    headers = {"Content-Type" = "application/json"}
    body = "{}"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    data_format = "json"
    json_string_fields = ["synced", "syncing"]
    tagexclude = ["url"]

[[inputs.http]]
    name_override = "http-chia"
    urls = [
         "https://localhost:8560/get_plot_directories",
         "https://localhost:9256/get_height_info",
         "https://localhost:9256/get_farmed_amount",
         "https://localhost:9256/get_wallet_balance",
         "https://localhost:8559/get_signage_point",
         "https://localhost:8560/refresh_plots",
    ]
    method = "POST"
    headers = {"Content-Type" = "application/json"}
    body = "{}"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    data_format = "json"
    tagexclude = ["url"]

[[inputs.http]]
    name_override = "http-chia"
    urls = [
         "{{ api_lfdm }}/{{ launcher_id }}"
    ]
    method = "GET"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    data_format = "json"
    tagexclude = ["url"]

[[inputs.http]]
    name_override = "http-chia"
    urls = [
         "https://localhost:8559/get_signage_points",
    ]
    method = "POST"
    headers = {"Content-Type" = "application/json"}
    body = "{}"
    tls_cert = "{{ chia_private_full_node_crt_path }}"
    tls_key = "{{ chia_private_full_node_key_path }}"
    insecure_skip_verify = true
    data_format = "json"
    json_query = "signage_points.#.signage_point"
    json_string_fields = ["reward_chain_sp", "challenge_chain_sp", "challenge_hash"]
    tagexclude = ["url"]
{% endif %}

{% if t_rex_enabled %}
[[inputs.http]]
    urls = [
        "http://127.0.0.1:4067/summary"
    ]
    method = "GET"
    data_format = "json"
{% endif %}

{% if os_is_linux %}
# Read metrics about cpu usage
[[inputs.cpu]]
  percpu = false
  totalcpu = true
  collect_cpu_time = false
  report_active = true

[[inputs.diskio]]
  devices = ["sda2", "md0", "nvme0n1", "nvme1n1", "sdb1", "sdc1", "sdd1", "sde1", "sdf1", "sdg1", "sdh1", "sdi1", "md1", "sdj1", "sdk1", "sdl1", "sdm1", "md2", "sdn1", "md3", "sdo1", "md1", "md4", "sdp1", "sdq1"]
  device_tags = ["ID_MODEL", "ID_REVISION", "ID_FS_LABEL"]

[[inputs.disk]]
  interval = "10m"
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]

[[inputs.mem]]

[[inputs.temp]]

[[inputs.hddtemp]]

[[inputs.procstat]]
  pattern = "chia_plot"
  process_name = "chia-plot"

{% endif %}

'''


class JinjaMaker:
    es_username = None
    es_password = None
    es_host_list = [
        "https://grafana.ether-source.fr:9201",
        "https://grafana.ether-source.fr:9202",
        "https://grafana.ether-source.fr:9203"
        ]
    name = ""
    telegraf_log_file_path = None
    os_is_windows = True
    os_is_linux = False
    custom_process_enabled = False
    process_list_to_harvest = ["telegraf"]
    nvidia_smi_enabled = False
    nvidia_smi_bin_path = None
    chia_collect_info_enabled = False
    launcher_id = None
    chia_private_full_node_crt_path = None
    chia_private_full_node_key_path = None
    t_rex_enabled = False
    api_lfdm = None

    def __init__(self):
        pass

    def SetEsUsername(self, username):
        self.es_username = username

    def SetEsPassword(self, password):
        self.es_password = password

    def SetSmiBinPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaCrtPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaKeyPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetCustomName(self, customName):
        self.name = customName

    def SetLaucherId(self, launcher_id):
        self.launcher_id = launcher_id

    def SetOsIsWindows(self, radio):
        if radio:
            self.os_windows = True
        else:
            self.os_windows = False

    def SetOsIsLinux(self, radio):
        if radio:
            self.os_linux = True
        else:
            self.os_linux = False

    def SetSmiEnable(self, state):
        if (Qt.Checked == state):
            self.nvidia_smi_enabled = True
        else:
            self.nvidia_smi_enabled = False

    def SetCollectChiaEnable(self, state):
        if (Qt.Checked == state):
            self.chia_collect_info_enabled = True
        else:
            self.chia_collect_info_enabled = False

    def GetCollectChiaEnable(self):
        return self.chia_collect_info_enabled

    def SetTrexEnable(self, state):
        if (Qt.Checked == state):
            self.t_rex_enabled = True
        else:
            self.t_rex_enabled = False

    def SetCustomProcessEnable(self, state):
        if (Qt.Checked == state):
            self.custom_process_enabled = True
        else:
            self.custom_process_enabled = False

    def GetCustomProcessEnable(self):
        return self.custom_process_enabled

    def SetTelegrafLogFilePath(self, telegraf_log_file_path):
        self.telegraf_log_file_path = telegraf_log_file_path

    def AppendToProcessList(self, process_list_to_harvest):
        tmpList = process_list_to_harvest.split(' ')
        for item in tmpList:
            self.process_list_to_harvest.append(item)

    def GenerateTemplate(self):
        template = Template(template_jinja)
        data_template = {
            "es_username": self.es_username,
            "es_password": self.es_password,
            "es_host_list": self.es_host_list,
            "name": self.name,
            "telegraf_log_file_path": self.telegraf_log_file_path,
            "os_is_windows": self.os_is_windows,
            "os_is_linux": self.os_is_linux,
            "custom_process_enabled": self.custom_process_enabled,
            "process_list_to_harvest": self.process_list_to_harvest,
            "nvidia_smi_enabled": self.nvidia_smi_enabled,
            "nvidia_smi_bin_path": self.nvidia_smi_bin_path,
            "chia_collect_info_enabled": self.nvidia_smi_bin_path,
            "launcher_id": self.launcher_id,
            "chia_private_full_node_crt_path": self.chia_private_full_node_crt_path,
            "chia_private_full_node_key_path": self.chia_private_full_node_key_path,
            "t_rex_enabled": self.t_rex_enabled,
            "api_lfdm": self.api_lfdm,
            }
        output_from_parsed_template = template.render(data_template)
        with open("telegraf.conf", "w") as fh:
            fh.write(output_from_parsed_template)
        fd = QFile(":/cafile/ether-source.pem")
        if fd.open(QIODevice.ReadOnly | QFile.Text):
            with open("ether-source.pem", "w") as fh:
                fh.write(QTextStream(fd).readAll())
            fd.close()
