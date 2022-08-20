import re

from yaml import parse


def flatten_config(self, config):
        parsers = [
            re.compile(
                r"""
                ^configure\sbridge\s(?P<negate_ageing_time>no\sageing-time)|(ageing-time\s(?P<ageing_time>\S+))$
                """, re.VERBOSE),
            re.compile(
                r"""
                configure\sbridge\sport\s(?P<id>\S+)\svlan-tpid0\s(?P<vlan_tpid0>\d+)
                (?P<negate_tpid>no tpid )?(tpid (?P<tpid>\S+))?
                $""", re.VERBOSE),
            re.compile(
                r"""
                configure\sbridge\sport\s(?P<id>\S+)\svlan-tpid1\s(?P<vlan_tpid1>\d+)
                (?P<negate_tpid>no tpid )?(tpid (?P<tpid>\S+))?
                $""", re.VERBOSE),
            re.compile(
                r"""
                configure\sbridge\sport\s(?P<id>\S+)\s
                ((?P<negate_default_priority>no default-priority)\s?)?((?P<default_priority>default-priority)\s?)?
                ((?P<negate_mac_learn_off>no mac-learn-off)\s?)?((?P<mac_learn_off>mac-learn-off)\s?)?
                ((?P<negate_max_unicast_mac>no max-unicast-mac)\s?)?(max-unicast-mac (?P<max_unicast_mac>\d)\s?)?
                ((?P<negate_qos_profile>no qos-profile)\s?)?(qos-profile (?P<qos_profile>\S+)\s?)?
                ((?P<negate_prio_regen_prof>no prio-regen-prof)\s?)?(prio-regen-prof (?P<prio_regen_prof>\S+)\s?)?
                ((?P<negate_prio_regen_name>no prio-regen-name)\s?)?(prio-regen-name (?P<prio_regen_name>\S+)\s?)?
                ((?P<negate_max_comitted_mac>no max-committed-mac)\s?)?(max-committed-mac (?P<max_committed_mac>\d+)\s?)?
                ((?P<negate_mirror_mode>no mirror-mode)\s?)?(mirror-mode (?P<mirror_mode>\S+)\s?)?
                ((?P<negate_mirror_vlan>no mirror-vlan)\s?)?(mirror-vlan (?P<mirror_vlan>\d+)\s?)?
                ((?P<negate_outervlancapture>no outervlancapture)\s?)?(outervlancapture (?P<outervlancapture>\d+)\s?)?
                ((?P<negate_direction>no direction)\s?)?(direction ((?P<direction>\d+)\s?))?
                ((?P<negate_pvid_tagging_flag>no pvid-tagging-flag)\s?)?(pvid-tagging-flag (?P<pvid_tagging_flag>\d+)\s?)?
                ((?P<negate_ds_pbit_mode>no ds-pbit-mode)\s?)?(ds-pbit-mode (?P<ds_pbit_mode>\d+)\s?)?
                ((?P<negate_default_tpid>no default-tpid)\s?)?(default-tpid (?P<default_tpid>\d+)\s?)?
                """, re.VERBOSE),
            re.compile(
                r"""
                configure\sbridge\sport\s(?P<id>\S+)\s
                vlan-id (?P<vlan_id>\d+)\s
                ((?P<negate_tag>no tag)\s?)?(tag\s(?P<tag>\S+)\s?)?
                ((?P<negate_l2fwder_vlan>no l2fwder-vlan)\s?)?(l2fwder-vlan\s(?P<l2fwder_vlan>\S+)\s?)?
                ((?P<negate_vlan_scope>no vlan-scope)\s?)?(vlan-scope\s(?P<vlan_scope>\S+)\s?)?
                ((?P<negate_qos>no qos)\s?)?(qos\s(?P<qos>\S+)\s?)?
                ((?P<negate_qos_profile>no qos-profile)\s?)?(qos-profile\s(?P<qos_profile>\S+)\s?)?
                ((?P<negate_prior_best_effort>no prior-best-effort)\s?)?((?P<prior_best_effort>prior-best-effort)\s?)?
                ((?P<negate_prior_background>no prior-background)\s?)?((?P<prior_background>prior-background)\s?)?
                ((?P<negate_prior_spare>no prior-spare)\s?)?((?P<prior_spare>prior-spare)\s?)?
                ((?P<negate_prior_exc_effort>no prior-exc-effort)\s?)?((?P<prior_exc_effort>prior-exc-effort)\s?)?
                ((?P<negate_prior_ctrl_load>no prior-ctrl-load)\s?)?((?P<prior_ctrl_load>prior-ctrl-load)\s?)?
                ((?P<negate_prior_less_100ms>no prior-less-100ms)\s?)?((?P<prior_less_100ms>prior-less-100ms)\s?)?
                ((?P<negate_prior_less_10ms>no prior-less-10ms)\s?)?((?P<prior_less_10ms>prior-less-10ms)\s?)?
                ((?P<negate_prior_nw_ctrl>no prior-nw-ctrl)\s?)?((?P<prior_nw_ctrl>prior-nw-ctrl)\s?)?
                ((?P<negate_in_qos_prof_name>no in-qos-prof-name)\s?)?(in-qos-prof-name\s(?P<in_qos_prof_name>\S+)\s?)?
                ((?P<negate_max_up_qos_policy>no max-up-qos-policy)\s?)?(max-up-qos-policy\s(?P<max_up_qos_policy>\d+)\s?)?
                ((?P<negate_max_ip_antispoof>no max-ip-antispoof)\s?)?(max-ip-antispoof\s(?P<max_ip_antispoof>\d+)\s?)?
                ((?P<negate_max_unicast_mac>no max-unicast-mac)\s?)?(max-unicast-mac\s(?P<max_unicast_mac>\d+)\s?)?
                ((?P<negate_max_ipv6_antispf>no max-ipv6-antispf)\s?)?(max-ipv6-antispf\s(?P<max_ipv6_antispf>\d+)\s?)?
                ((?P<negate_mac_learn_ctrl>no mac-learn-ctrl)\s?)?(mac-learn-ctrl\s(?P<mac_learn_ctrl>\d+)\s?)?
                ((?P<negate_min_cvlan_id>no min-cvlan-id)\s?)?(min-cvlan-id\s(?P<min_cvlan_id>\d+)\s?)?
                ((?P<negate_max_cvlan_id>no max-cvlan-id)\s?)?(max-cvlan-id\s(?P<max_cvlan_id>\d+)\s?)?
                ((?P<negate_ds_dedicated_q>no ds-dedicated-q)\s?)?((?P<ds_dedicated_q>ds-dedicated-q)\s?)?
                ((?P<negate_tpid>no tpid)\s)?(tpid\s(?P<tpid>\S+)\s?)?
                ((?P<negate_inner_pbit_remark>no inner-pbit-remark)\s?)?(inner-pbit-remark\s(?P<inner_pbit_remark>\S+)\s?)?
                ((?P<negate_groupid>no groupid)\s?)?(groupid\s(?P<groupid>\d+)\s?)?
                ((?P<negate_usacceptframetype>no usacceptframetype)\s?)?(usacceptframetype\s(?P<usacceptframetype>\S+)\s?)?
                ((?P<negate_oltregenprofile>no oltregenprofile)\s?)?((?P<oltregenprofile>oltregenprofile)\s?)?
                $""", re.VERBOSE),
            re.compile(
                r"""
                configure\sbridge\sport\s(?P<id>\S+)\s
                ((?P<negate_pvid>no pvid))|(pvid\s(?P<pvid>\S+)s?)
                $""", re.VERBOSE),
            ]
        flattened_config = []
        vlan_id = None
        bridge_id = None
        for line in config.splitlines():
            # if line contains bridge port id, store it in bridge_id
            for regex in parsers:
                match = regex.match(line)
                if match:
                    bridge_id = match.group('id')
                    if match.group('vlan_id'):
                        vlan_id = match.group('vlan_id')
                    # for each group matched, add it to the flattened config and prepend the bridge_id. Also prepend vlan_id if it exists
                    for group in match.groupdict().keys():
                        if match.group(group):
                            if vlan_id:
                                flattened_config.append('configure bridge port ' + bridge_id  + ' ' +  vlan_id + ' ' + match.group(group))
                            else:
                                flattened_config.append('configure bridge port ' + bridge_id + ' ' + match.group(group))
                    break
          
                

teststring = """configure bridge port 1/1/8/35 no default-priority no mac-learn-off max-unicast-mac 5 qos-profile name:qpsUP10Mbps no prio-regen-prof no prio-regen-name no max-committed-mac no mirror-mode no mirror-vlan no outervlancapture no direction no pvid-tagging-flag no ds-pbit-mode no default-tpid
configure bridge port 1/1/8/35 vlan-tpid0 0 no tpid
configure bridge port 1/1/8/35 vlan-tpid1 1 no tpid
configure bridge port 1/1/8/35 vlan-id 10 tag single-tagged l2fwder-vlan 310 vlan-scope local no qos no qos-profile no prior-best-effort no prior-background no prior-spare no prior-exc-effort no prior-ctrl-load no prior-less-100ms no prior-less-10ms no prior-nw-ctrl no in-qos-prof-name no max-up-qos-policy no max-ip-antispoof no max-unicast-mac no max-ipv6-antispf no mac-learn-ctrl no min-cvlan-id no max-cvlan-id no ds-dedicated-q no tpid no inner-pbit-remark no groupid no usacceptframetype no oltregenprofile
configure bridge port 1/1/8/35 no pvid
configure bridge port 1/1/8/36 no default-priority no mac-learn-off max-unicast-mac 5 qos-profile name:qpsUP10Mbps no prio-regen-prof no prio-regen-name no max-committed-mac no mirror-mode no mirror-vlan no outervlancapture no direction no pvid-tagging-flag no ds-pbit-mode no default-tpid
configure bridge port 1/1/8/36 vlan-tpid0 0 no tpid
configure bridge port 1/1/8/36 vlan-tpid1 1 no tpid
configure bridge port 1/1/8/36 vlan-id 10 tag single-tagged l2fwder-vlan 310 vlan-scope local no qos no qos-profile no prior-best-effort no prior-background no prior-spare no prior-exc-effort no prior-ctrl-load no prior-less-100ms no prior-less-10ms no prior-nw-ctrl no in-qos-prof-name no max-up-qos-policy no max-ip-antispoof no max-unicast-mac no max-ipv6-antispf no mac-learn-ctrl no min-cvlan-id no max-cvlan-id no ds-dedicated-q no tpid no inner-pbit-remark no groupid no usacceptframetype no oltregenprofile
configure bridge port 1/1/8/36 no pvid"""

flatten_config(teststring)