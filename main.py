from inc import glibrary as inc

def main():
  glib = inc.GLibrary()
  print ":".join(glib.create())

if __name__ == "__main__":
  main()