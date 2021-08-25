from pathlib import Path

master = Path(r"J:/")
mirrors = ["E:\PoolPart.fe737769-e6dc-41b1-a02d-2c7887a9de1f",
          "G:\PoolPart.3ee440bb-e162-479b-8d48-4196379d7702",
          "H:\PoolPart.9bae76d0-f67d-4662-8713-b0fb75bbadc2"]

def match_master_mirrors(master, slave, test=True):
    master = Path(master)
    slave = Path(slave)

    for p in master.rglob("*"):
        if p.is_dir():
            rel_path = p.relative_to(master)
            new_path = slave / rel_path
            if not new_path.exists():
                if test:
                    print(new_path)
                else:
                    try:
                        new_path.mkdir(exist_ok=True,parents=True)
                    except Exception as e:
                        print(e)

if __name__=='__main__':
    for sl in mirrors:
        match_master_mirrors(master, sl)
