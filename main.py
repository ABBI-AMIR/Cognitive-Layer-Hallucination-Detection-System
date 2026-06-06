from core.hallucination_detector import HallucinationDetector


def main():
    detector = HallucinationDetector()
    while True:
        q = input("Query (quit to exit): ")
        if q.lower() in ["quit", "exit"]:
            break
        result = detector.run(q)
        print("\nResponse:\n", result["response"])


if __name__ == "__main__":
    main()
