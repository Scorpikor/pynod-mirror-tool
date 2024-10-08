import random
import sys

def user_agent (ver):
    if ver == 'v3':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; BPC 4.5.12011.3; OS: 6.2.9200 SP 0.0 NT; TDB 62496; LUO 0.101; CH 0.0; LNG 1049; x64s; APP efsw; FW 0.0; PX 0; PUA 1; RA 0; UBR 7159; HVCI 0; SHA256 1; WU 3; ACS 1)',
        'ESS Update (Windows; U; 32bit; VDB 62496; BPC 4.5.12011.3; OS: 6.2.9200 SP 0.0 NT; TDB 62496; LUO 0.101; CH 0.0; LNG 1049; x64s; APP efsw; FW 0.0; PX 0; PUA 1; RA 0; UBR 7159; HVCI 0; SHA256 1; WU 3; ACS 1)'
        )
        return random.choice(bzz)

    if ver == 'v5':
        bzz =(
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; BPC 5.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01003AD8-8936-1E9B-4561-88243B38324B)',
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; BPC 5.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01002CD8-8936-1A8B-4561-88643B38A24B)'
        )
        return random.choice(bzz)

    if ver == 'ep11':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 2486; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 0100B9A0-42B1-1750-55DF-CAEB09DF8A91; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01004AA6-2EAC-D77C-67BC-20E6F05C6A1B; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19045 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 0; HWF: 01005E32-3BC2-517A-3422-4FC7D96C228D; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01006EA5-7B2D-F1B5-4AF4-0BE6460EBA88; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.14393 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 7259; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01009A9A-0E80-5B64-D3F6-777607621C5C; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        )
        return random.choice(bzz)

 
    else:
        print ("Неопределенная версия", ver, "в user_agent.py")
        sys.exit(1)