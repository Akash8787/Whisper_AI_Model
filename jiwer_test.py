import jiwer

reference = "the shipment arrives at Mundra port on 14 October"
hypothesis = "the shipment arrives at Mundra port on 14 October"

transform = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemovePunctuation(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.ReduceToListOfListOfWords(),
])

print("WER:", jiwer.wer(reference, hypothesis, reference_transform=transform, hypothesis_transform=transform))
print("CER:", jiwer.cer(reference, hypothesis))