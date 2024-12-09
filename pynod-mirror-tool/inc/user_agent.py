# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import random
import sys

def user_agent (ver):
    if ver == 'v3':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; BPC 4.5.12011.3; OS: 6.2.9200 SP 0.0 NT; TDB 62496; LUO 0.101; CH 0.0; LNG 1049;',
        'ESS Update (Windows; U; 32bit; VDB 62496; BPC 4.5.12011.3; OS: 6.2.9200 SP 0.0 NT; TDB 62496; LUO 0.101; CH 0.0; LNG 1049;',
        )
        return random.choice(bzz)

    if ver == 'v5':
        bzz =(
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 5.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01003AD8-8936-1E9B-4561-88243B38324B)',
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 5.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01002CD8-8936-1A8B-4561-88643B38A24B)'
        )
        return random.choice(bzz)
        
    if ver == 'v9':
        bzz =(
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 9.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01003AD8-8936-1E9B-4561-88243B38324B)',
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 9.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01002CD8-8936-1A8B-4561-88643B38A24B)'
        )
        return random.choice(bzz)

    if ver == 'v10':
        bzz =(
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 10.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01003AD8-8936-1E9B-4561-88243B38324B)',
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 10.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01002CD8-8936-1A8B-4561-88643B38A24B)'
        )
        return random.choice(bzz)
        
    if ver == 'v11':
        bzz =(
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 11.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01003AD8-8936-1E9B-4561-88243B38324B)',
        'ESS Update (Windows; U; 32bit; PVT F; VDB 15881; EAV 11.0.2225.1; OS: 6.2.9200 SP 0.0 NT; TDB 15881; CL 0.0.0; LNG 1049; x64c; APP eea; BEO 1; ASP 0.10; FW 0.0; PX 0; PUA 1; CD 0; RA 0; HWF: 01002CD8-8936-1A8B-4561-88643B38A24B)'
        )
        return random.choice(bzz)

    if ver == 'v12':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 12.0.12011.3; OS: 6.2.9200 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 12.0.12011.3; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)

    if ver == 'v13':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 13.0.12011.3; OS: 6.2.9200 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 13.0.12011.3; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)
        
    if ver == 'v14':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 14.0.12011.3; OS: 6.2.9200 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 14.0.12011.3; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)
        
    if ver == 'v15':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 15.0.12011.3; OS: 6.2.9200 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 15.0.12011.3; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)
 
    if ver == 'v16':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 16.0.12011.3; OS: 10.0.26100 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 16.0.12011.3; OS: 10.0.26100 SP 0.0 NT;'
        )
        return random.choice(bzz)    
 
    if ver == 'v18':
        bzz =(
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 18.0.11.0; OS: 10.0.19045 SP 0.0 NT;',
        'ESS Update (Windows; U; 32bit; VDB 62496; EAV 18.0.11.0; OS: 10.0.19045 SP 0.0 NT;'
        )
        return random.choice(bzz)
    
    if ver == 'ep6':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 6.0.2060.0; OS: 10.0.26100 SP 0.0 NT;',
        'EEA Update (Windows; U; 64bit; BPC 6.0.2062.0; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz) 
    
    if ver == 'ep7':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 7.0.2060.0; OS: 6.2.9200 SP 0.0 NT;',
        'EEA Update (Windows; U; 64bit; BPC 7.0.2062.0; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)
    
    if ver == 'ep8':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 8.0.2060.0; OS: 6.2.9200 SP 0.0 NT;',
        'EEA Update (Windows; U; 64bit; BPC 8.0.2062.0; OS: 6.2.9200 SP 0.0 NT;'
        )
        return random.choice(bzz)

    if ver == 'ep9':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 9.1.2060.0; OS: 10.0.26100 SP 0.0 NT; HWF: 01001E59-7926-48F0-8556-5209DC5E3C06; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 3AC-9SP-9D9; SEAT 154b3474; RET 2103)',
        'EEA Update (Windows; U; 64bit; BPC 9.1.2060.0; OS: 10.0.26100 SP 0.0 NT; HWF: 01001E58-7916-38F1-8218-2208DC5E3C12; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 2AC-2SP-9D9; SEAT 144b2454; RET 2103)',
        )
        return random.choice(bzz)
        
    if ver == 'ep10':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 10.1.2050.0; OS: 10.0.26100 SP 0.0 NT; HWF: 01001E59-7926-48F0-8532-3209DC5E3C06; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 3AC-9SP-9D9; SEAT 142a2374; RET 2103)',
        'EEA Update (Windows; U; 64bit; BPC 10.1.2050.0; OS: 10.0.26100 SP 0.0 NT; HWF: 01001B48-6812-17C0-7423-4209DC5E3C06; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 3BA-8SP-8D9; SEAT 125b3772; RET 2103)',
        )
        return random.choice(bzz)

    if ver == 'ep11':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 2486; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 0100B9A0-42B1-1750-55DF-CAEB09DF8A91; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01004AA6-2EAC-D77C-67BC-20E6F05C6A1B; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19045 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 0; HWF: 01005E32-3BC2-517A-3422-4FC7D96C228D; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.19044 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 4780; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01006EA5-7B2D-F1B5-4AF4-0BE6460EBA88; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2039.2; OS: 10.0.14393 SP 0.0 NT; TDB 62700; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 7259; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01009A9A-0E80-5B64-D3F6-777607621C5C; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 33D-58A-6KA; SEAT 154b3474; RET 5003)',
        'EEA Update (Windows; U; 64bit; BPC 11.1.2052.0; OS: 10.0.26100 SP 0.0 NT; TDB 63278; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 1882; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; HWF: 01001E59-7926-48F0-8538-5209DC5E3C06; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 3AC-9SP-9D9; SEAT 154b3474; RET 5003)',
        )
        return random.choice(bzz)
        
    if ver == 'ep12':
        bzz =(
        'EEA Update (Windows; U; 64bit; BPC 12.0.2038.0; OS: 10.0.19044 SP 0.0 NT; Mirror; TDB 63712; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 5131; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; NPU 0; HWF: 01002113-CA24-DFF1-C386-8730C979CAFA; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 32D-58A-5KA; SEAT 143b3474; RET 2103)',
        'EEA Update (Windows; U; 64bit; BPC 12.0.2038.0; OS: 10.0.19044 SP 0.0 NT; Mirror; TDB 63712; CL 0.0.0; x64c; APP eea; PX 0; PUA 1; CD 0; RA 0; UNS 1; UBR 5131; HVCI 0; SHA256 1; WU 3; ACS 1; TDT 0; LTS 1; NPU 0; HWF: 01016223-CC15-AFF1-C285-6720C974CAFE; PLOC ru_ru; PCODE 107.0.0; PAR -1; ATH -1; DC 0; PLID 21D-46A-AKA; SEAT 124b3434; RET 2103)'
            )
        return random.choice(bzz)
    
    else:
        print ("Неопределенная версия", ver, "в user_agent.py")
        sys.exit(1)