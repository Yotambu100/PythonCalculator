from controller import Controller

if __name__ == '__main__':
    try:
        controller = Controller()
        controller.run()
    except KeyboardInterrupt:
        print("program interrupted by user\nexiting....")
