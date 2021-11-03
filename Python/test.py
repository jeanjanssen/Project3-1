from GameAITicTacToe import GameAITicTacToe

def main():
    g = GameAITicTacToe()

    root = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

    g.createTree(root, 1) # 1 is for X, 2 for O

    print(len(g.edges))
    print(len(g.nodes))
    print(g.generationCounter)
    calcul = 1+9+(9*8)+(9*8*7)+(9*8*7*6)+(9*8*7*6*5)+(9*8*7*6*5*4)+(9*8*7*6*5*4*3)+(9*8*7*6*5*4*3*2)+(9*8*7*6*5*4*3*2*1)
    print('expected', calcul)

if __name__ == '__main__':
    main()

